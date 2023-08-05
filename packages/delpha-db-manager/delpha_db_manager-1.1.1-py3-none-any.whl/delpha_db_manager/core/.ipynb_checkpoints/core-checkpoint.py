from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
from simple_salesforce import Salesforce
import requests
from datetime import datetime
import os
import time
import random
import json
import string
import pandas as pd
from boto3.session import Session
import boto3
from delpha_db_manager.utils.aws import start_appflow, start_s3
import uuid
import io


class CassandraManager:
    """
    Cassandra Cluster center
    :param username: String Cassandra username to connect
    :param password: String password username to connect
    :param pem_file_path: String path of the .pem file to use for 2FA connection
    :param key_space: String session keyspace to set for the Cluster
    """
    def __init__(self, username, password, pem_file_path, key_space='delpha_actions'):
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.load_verify_locations(pem_file_path)
        ssl_context.verify_mode = CERT_REQUIRED
        ssl_context.check_hostname = True

        cassandra_username = os.environ.get('CASSANDRA_USERNAME', username)
        cassandra_password = os.environ.get('CASSANDRA_PWD', password)
        cassandra_dc1 = os.environ.get('CASSANDRA_DC1', 'DATACENTER_EU_WEST_1')
        cassandra_node1 = os.environ.get('CASSANDRA_NODE1', '52.215.22.60')
        cassandra_node2 = os.environ.get('CASSANDRA_NODE2', '34.254.52.140')
        cassandra_node3 = os.environ.get('CASSANDRA_NODE3', '34.251.123.6')

        self._cluster = Cluster(
            [
                cassandra_node1, cassandra_node2, cassandra_node3
            ],
            load_balancing_policy=DCAwareRoundRobinPolicy(local_dc=cassandra_dc1),
            port=9042,
            auth_provider=PlainTextAuthProvider(
                username=cassandra_username,
                password=cassandra_password
            ),
            ssl_context=ssl_context
        )
        self._keyspace = key_space
        self._session = self._cluster.connect(key_space)
        self._session.row_factory = dict_factory
        print('Connected to cluster %s' % self._cluster.metadata.cluster_name)
        for host in self._cluster.metadata.all_hosts():
            print('Datacenter: %s; Host: %s; Rack: %s' % (host.datacenter, host.address, host.rack))

    def __del__(self):
        self._cluster.shutdown()

    def disconnect(self):
        print("Cluster is disconnected !")
        self._cluster.shutdown()

    @property
    def cluster(self):
        return self._cluster

    @property
    def session(self):
        return self._session

    @property
    def keyspace(self):
        return self._keyspace
    
    def set_keyspace(self, key_space):
        self._keyspace = key_space
        self._session.set_keyspace(key_space)

    def execute(self, query_string, *args, **kwargs):
        """
        Execute a cql command, as a blocking call that will not return until the statement is finished executing.
        :param query_string: query executed
        """
        return self._session.execute(query_string, *args, **kwargs)

    def execute_async(self, query_string, *args, **kwargs):
        """
        Execute a cql command asynchronously (program continues and getting a future_response)
        :param query_string: query executed
        """
        return self._session.execute_async(query_string, *args, **kwargs)

    
class SalesforceManager:
    """
    Salesforce Manager
    :param instance_name: Salesforce Instance name
    :param client_id: Consumer ID for authorized app
    :param client_secret: Consumer Secret for authorized app
    :param username: usernam to login to Instance of Salesforce
    :param password: password to login to Instance of Salesforce
    :param security_token: User's security token
    """
    def __init__(self, instance_name, client_id, client_secret, username, password, security_token):
        print("Connecting to Salesforce...")
        params = {
            "grant_type": "password",
            "client_id": client_id, # Consumer Key
            "client_secret": client_secret, # Consumer Secret
            "username": username,
            "password": password+security_token
        }
        r = requests.post(f"https://{instance_name}.my.salesforce.com/services/oauth2/token", params=params)
        self.access_token = r.json().get("access_token")
        self.instance_url = r.json().get("instance_url")
        self.headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % self.access_token
        }
        print(r.json())
        self.api_url = self.instance_url+'/services/data/v51.0/'
        self.describe_columns = ["name", "label", "type", "custom", "referenceTo", ]
        print("Credentials acquired !")

    def help(self):
        sf_url = self.api_url
        r = requests.request('get', self.api_url, headers=self.headers)
        if r.status_code < 300:
            return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
            
    def execute(self, api_route, method="get", params={}, data={}):
        """
        Generalized execute system for Salesforce API
        :param api_route: api route to use
        :param params: Object to send to the API as additive data
        """
        sf_url = self.api_url + f'{api_route}'
        
        if method == 'get':
            r = requests.request('get', sf_url, headers=self.headers, params=params)
        else:
            r = requests.request(method, sf_url, headers=self.headers, json=data, params=parameters, timeout=10)
        if r.status_code < 300:
            return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
        
    def query(self, query, to_pandas=True):
        """
        Simple query system for Salesforce
        :param query: String SOQL query to run
        """
        parameters = {
            'q': query
        }
        sf_url = self.api_url + 'query/'
        r = requests.request('get', sf_url, headers=self.headers, params=parameters)
        results = []
        if r.status_code < 300:
            curr_results = r.json()
            results = curr_results
            while curr_results.get("nextRecordsUrl"):
                next_r = self._query_next(curr_results.get("nextRecordsUrl").split('/')[-1:][0])
                curr_results = next_r
                results["records"] = [*results["records"], *curr_results["records"]]
            if to_pandas:
                return pd.DataFrame(results["records"]), results["totalSize"]
            else:
                return results["records"], results["totalSize"]
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
            
    def _query_next(self, next_url):
        sf_url = self.api_url + 'query/' + next_url
        r = requests.request('get', sf_url, headers=self.headers)
        if r.status_code < 300:
            curr_results = r.json()
            return curr_results
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
        return 
            
    def describe_object(self, sf_object, to_pandas=True):
        """
        Describe a Salesforce object
        :param sf_object: String Saleforce object name to describe
        :param to_pandas: Boolean to set pandas dataframe result or not
        """
        sf_url = self.api_url + f'sobjects/{sf_object}/describe'
        r = requests.request('get', sf_url, headers=self.headers)
        if r.status_code < 300:
            if to_pandas:
                return pd.DataFrame(r.json()["fields"])[self.describe_columns]
            else:
                return r.json()["fields"]
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
         
    def search(self, search_q, to_pandas=True):
        """
        Simple search system for Salesforce
        :param search_q: search item to look for
        """
        parameters = {
            'q': "FIND {"+search_q+"}"
        }
        
        sf_url = self.api_url + 'search/'
        r = requests.request('get', sf_url, headers=self.headers, params=parameters)
        if r.status_code < 300:
            if to_pandas:
                return pd.DataFrame(r.json()["searchRecords"])
            else:
                return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))     

    def get_record(self, record_id, record_type, to_pandas=True):
        """
        Get a Salesforce record from Salesforce
        :param record_id: String Saleforce object Id to get
        :param record_type: String Saleforce object name to get
        """
        sf_url = self.api_url + f'sobjects/{record_type}/{record_id}'
        r = requests.request('get', sf_url, headers=self.headers)
        if r.status_code < 300:
            if to_pandas:
                return pd.DataFrame(r.json())[self.describe_columns]
            else:
                return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
            
    def insert(self, object_name, data={}, parameters={}, to_pandas=True):
        """
        Simple Insert system of Salesforce
        :param object_name: String object to insert data into
        :param data: Dict data to insert json
        :param parameters: Dict Parameters of request 
        """
        sf_url = self.api_url + 'sobjects/' + object_name + "/"
        r = requests.request('post', sf_url, headers=self.headers, json=data, params=parameters, timeout=10)
        if r.status_code < 300:
            return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
            
            
class AppFlowManager:
    """
    Delpha AWS Salesforce data Handler
    :param key: String AWS key
    :param secret: String AWS secret
    :param flow_type: String Flow type to handle ['contact', 'account']
    :param region: String AWS region 
    """
    def __init__(self, key, secret, flow_type, region='us-east-2'):
        self.s3_handler = start_s3(key, secret, region)
        self.flow_handler = start_appflow(key, secret, region)
        self.buckets = None
        self.settings = {}
        self.current_settings = {}
        self._load_settings(flow_type)
        
    def _load_settings(self, flow_type):
        """
        Load buckets name from AWS
        """
        buckets = self.s3_handler.list_buckets()
        self.buckets = [bucket["Name"] for bucket in buckets["Buckets"]]
        self.settings = json.loads(self.s3_handler.get_object(Bucket=self.buckets[0], Key = "config/flow_settings.json")["Body"].read().decode('utf-8'))
        self.current_settings = self.settings[flow_type]
        self.current_settings["bucket_name"] = self.buckets[0]
        
    def set_flow_settings(self, flow_type):
        """
        Set flow configuration
        :param flow_type: String Flow type to be used ['contact', 'account']
        """
        self.current_settings = self.settings[flow_type]
        self.current_settings["bucket_name"] = self.buckets[0]
        
    def list_objects(self, bucket_name=None):
        """
        List all AWS object in S3 bucket
        :param bucket_name: String Bucket name to retrieve object from
        """
        if not isinstance(bucket_name, str):
            bucket_name = self.current_settings["bucket_name"]
        all_objects = self.s3_handler.list_objects(Bucket = bucket_name, Prefix = "Salesforce/Objects/", Delimiter = '/')
        all_objects = [prefix["Prefix"] for prefix in all_objects["CommonPrefixes"]]
        return all_objects
    
    def list_files(self, bucket_name=None, prefix=None):
        """
        List all files available within a bucket, regarding a certain prefix
        :param bucket_name: String Bucket name to retrieve files from
        :param prefix: String prefix path to use for file retrieval
        """
        if not isinstance(bucket_name, str):
            bucket_name = self.current_settings["bucket_name"]
        if not isinstance(prefix, str):
            prefix = self.current_settings["prefix"]
        list_obj = []
        kwargs = {'Bucket': bucket_name}
        if isinstance(prefix, str):
                kwargs['Prefix'] = prefix
        while True:
                resp = self.s3_handler.list_objects_v2(**kwargs)
                for obj in resp['Contents']:
                    key = obj['Key']
                    if key.startswith(prefix):
                        list_obj.append(key)
                try:
                    kwargs['ContinuationToken'] = resp['NextContinuationToken']
                except KeyError:
                    break
        return list_obj
    
    def get_flow_parquet_data(self, bucket_name=None, prefix=None, flow_name=None):
        """
        Load Flow data in a pd.DataFrame object
        :param bucket_name: String Bucket name to retrieve data from
        :param prefix: String prefix path to use for data retrieval
        :param flow_name: String Flow name to use
        """
        if not isinstance(bucket_name, str):
            bucket_name = self.current_settings["bucket_name"]
        if not isinstance(prefix, str):
            prefix = self.current_settings["prefix"]
        if not isinstance(flow_name, str):
            flow_name = self.current_settings["flow_name"]
        last_flow = self.get_last_flow_id(flow_name)
        file_folder = prefix+last_flow
        file_keys = handler.list_files(prefix=file_folder)
        def pd_read_s3_parquet(key, **args):
            print(key)
            obj = self.s3_handler.get_object(Bucket=self.current_settings["bucket_name"], Key=key)
            return pd.read_parquet(io.BytesIO(obj['Body'].read()), **args)
        dfs = [pd_read_s3_parquet(key=key) 
           for key in file_keys]
        
        return pd.concat(dfs, ignore_index=True)
    
    def start_flow(self, flow_name):
        """
        Start a Flow Process
        :param flow_name: String Name of the flow to trigger
        """
        flow_start_response = self.flow_handler.start_flow(flowName=flow_name)
        flow_status = flow_start_response["ResponseMetadata"]["HTTPStatusCode"]
        flow_last_execution_record = flow_start_response['executionId']
        return flow_status, flow_last_execution_record
    
    def ensure_spark_format(self, flow_name):
        """
        Function to be called on Spark loading to make sure data is in good format
        :param flow_name: String AppFlow name to be checked
        """
        prefix = self.current_settings["prefix"]
        last_flow = self.get_last_flow_id(flow_name)
        file_folder = prefix+last_flow
        file_keys = handler.list_files(prefix=file_folder)
        if any(".parquet" in s for s in file_keys):
            return True
        else:
            for key in file_keys:
                self.s3_handler.copy_object(Bucket=self.current_settings['bucket_name'], CopySource="/"+self.current_settings['bucket_name']+"/"+key, Key=file_folder+"/"+str(uuid.uuid4())+".parquet")
                self.s3_handler.delete_object(Bucket=self.current_settings['bucket_name'], Key=key)
        return True
    
    def get_last_flow_id(self, flow_name):
        """
        Get last folder ID for the requested flow
        :param flow_name: String AppFlow name to be checked
        """
        return self.flow_handler.describe_flow_execution_records(flowName=flow_name)["flowExecutions"].pop(0)["executionId"]

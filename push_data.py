import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()# this is used to access the environment variables defined in the .env file at project level

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

# This is used to verify the critificates of the websites while making a connection to the site
import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo

#importing modules from other files which will be used for exception handling and logging 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#This class is used to extract the data from network/local files , convert the data and then push to the mongodb server
class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def cv_to_jason_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            #now we will convert our data records into list of json
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
       
#This is the main execution instructions to execute and test the ELT process       
if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE = "VANDANAI"
    Collection="NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_jason_convertor(file_path=FILE_PATH)# creating the class object to do the operation
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records=records,database=DATABASE,collection=Collection)
    print(no_of_records)

        
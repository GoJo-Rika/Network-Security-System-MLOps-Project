import json
import os
import sys
from urllib.parse import quote_plus

import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

load_dotenv()
username = os.getenv("MONGO_DB_USERNAME")
password = os.getenv("MONGO_DB_PASSWORD")

username = quote_plus(username)
password = quote_plus(password)

MONGO_DB_URL: str = f"mongodb+srv://{username}:{password}@cluster0.l5ee6dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
print(MONGO_DB_URL)

ca = certifi.where()


class NetworkSecurityExtract:
    def __init__(self) -> None:
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path: str) -> list:
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records: list, database: str, collection: str) -> int:
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "TEST_DB"
    Collection = "NetworkData"
    networkobj = NetworkSecurityExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)

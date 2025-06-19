import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import pymongo
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from network_security.entity.artifact_entity import DataIngestionArtifact

## Configuration of the Data Ingestion Config
from network_security.entity.config_entity import DataIngestionConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

load_dotenv()

username = os.getenv("MONGO_DB_USERNAME")
password = os.getenv("MONGO_DB_PASSWORD")

username = quote_plus(username)
password = quote_plus(password)

MONGO_DB_URL: str = f"mongodb+srv://{username}:{password}@cluster0.l5ee6dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """Read data from mongodb."""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = Path(feature_store_file_path).parent
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio,
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class",
            )
            dir_path = Path(self.data_ingestion_config.training_file_path).parent

            Path(dir_path).mkdir(parents=True, exist_ok=True)
            Path(dir_path).mkdir(parents=True, exist_ok=True)

            logging.info("Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True,
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True,
            )
            logging.info("Exported train and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException

import sys
from pathlib import Path

import pandas as pd
from scipy.stats import ks_2samp

from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self._numerical_columns = self._schema_config.get("numerical_columns", [])
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            return len(dataframe.columns) == number_of_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        """
        Validates whether all required numerical columns exist in the given DataFrame.

        Returns:
            bool: True if all required numerical columns exist and are numeric, False otherwise.

        """
        try:
            required_numerical_columns = self._numerical_columns
            missing_columns = []
            non_numeric_columns = []

            for column in required_numerical_columns:
                if column not in dataframe.columns:
                    missing_columns.append(column)
                elif not pd.api.types.is_numeric_dtype(dataframe[column]):
                    non_numeric_columns.append(column)

            if missing_columns:
                logging.info(f"Missing numerical columns: {missing_columns}")
            if non_numeric_columns:
                logging.info(f"Columns not of numeric type: {non_numeric_columns}")

            return len(missing_columns) == 0 and len(non_numeric_columns) == 0

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold: float = 0.05) -> bool:
        try:
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                is_found = not threshold <= is_same_dist.pvalue
                report.update(
                    {
                        column: {
                            "p_value": float(is_same_dist.pvalue),
                            "drift_status": is_found,
                        },
                    },
                )
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = Path(drift_report_file_path).parent
            dir_path.mkdir(parents=True, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            write_yaml_file(file_path=drift_report_file_path, content=report)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## Read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                logging.info("Train dataframe does not contain all columns.\n")

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                logging.info("Test dataframe does not contain all columns.\n")

            # Validate numerical columns
            status = self.validate_numerical_columns_exist(train_dataframe)
            if not status:
                logging.info("Train dataframe is missing required numerical columns or types.\n")

            status = self.validate_numerical_columns_exist(test_dataframe)
            if not status:
                logging.info("Test dataframe is missing required numerical columns or types.\n")

            ## Check data drift
            status = self.detect_dataset_drift(
                base_df=train_dataframe, current_df=test_dataframe)
            dir_path = Path(self.data_validation_config.valid_train_file_path).parent
            dir_path.mkdir(parents=True, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

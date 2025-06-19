from datetime import datetime
from pathlib import Path

from network_security.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig:
    def __init__(self, timestamp: datetime = None) -> None:
        if timestamp is None:
            timestamp = datetime.now().astimezone()
        timestamp_str = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = Path(self.artifact_name) / timestamp_str
        self.model_dir = Path("final_model")
        self.timestamp: str = timestamp_str


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:
        self.data_ingestion_dir: Path = (
            Path(training_pipeline_config.artifact_dir)
            / training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: Path = (
            self.data_ingestion_dir
            / training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
            / training_pipeline.FILE_NAME
        )
        self.training_file_path: Path = (
            self.data_ingestion_dir
            / training_pipeline.DATA_INGESTION_INGESTED_DIR
            / training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path: Path = (
            self.data_ingestion_dir
            / training_pipeline.DATA_INGESTION_INGESTED_DIR
            / training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        )
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME

## Model Training Testing
import sys

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_transformation import DataTransformation
from network_security.components.data_validation import DataValidation
from network_security.components.model_trainer import ModelTrainer
from network_security.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig,
)
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

if __name__ == "__main__":
    try:
        ### DATA INGESTION ###
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config,
        )
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiated data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(data_ingestion_artifact)

        ### DATA VALIDATION ###
        data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config,
        )
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        logging.info("Initiated data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)

        ### DATA TRANSFORMATION ###
        data_transformation_config = DataTransformationConfig(
            training_pipeline_config=training_pipeline_config,
        )
        data_transformation = DataTransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config,
        )
        logging.info("Initiated data transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

        ### MODEL TRAINING ###
        model_trainer_config = ModelTrainerConfig(
            training_pipeline_config=training_pipeline_config,
        )
        model_trainer = ModelTrainer(
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_config=model_trainer_config,
        )
        logging.info("Initiated model trainer")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Trainer Completed")
        print(model_trainer_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


## =============================================================

## Data Transformation Testing
# import sys

# from network_security.components.data_ingestion import DataIngestion
# from network_security.components.data_transformation import DataTransformation
# from network_security.components.data_validation import DataValidation
# from network_security.entity.config_entity import (
#     DataIngestionConfig,
#     DataTransformationConfig,
#     DataValidationConfig,
#     TrainingPipelineConfig,
# )
# from network_security.exception.exception import NetworkSecurityException
# from network_security.logging.logger import logging

# if __name__ == "__main__":
#     try:
#         ### DATA INGESTION ###
#         training_pipeline_config = TrainingPipelineConfig()
#         data_ingestion_config = DataIngestionConfig(
#             training_pipeline_config=training_pipeline_config,
#         )
#         data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
#         logging.info("Initiated data ingestion")
#         data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
#         logging.info("Data Initiation Completed")
#         print(data_ingestion_artifact)

#         ### DATA VALIDATION ###
#         data_validation_config = DataValidationConfig(
#             training_pipeline_config=training_pipeline_config,
#         )
#         data_validation = DataValidation(
#             data_ingestion_artifact=data_ingestion_artifact,
#             data_validation_config=data_validation_config,
#         )
#         logging.info("Initiated data validation")
#         data_validation_artifact = data_validation.initiate_data_validation()
#         logging.info("Data Validation Completed")
#         print(data_validation_artifact)

#         ### DATA TRANSFORMATION ###
#         data_transformation_config = DataTransformationConfig(
#             training_pipeline_config=training_pipeline_config,
#         )
#         data_transformation = DataTransformation(
#             data_validation_artifact=data_validation_artifact,
#             data_transformation_config=data_transformation_config,
#         )
#         logging.info("Initiated data transformation")
#         data_transformation_artifact = data_transformation.initiate_data_transformation()
#         logging.info("Data Transformation Completed")
#         print(data_transformation_artifact)


#     except Exception as e:
#         raise NetworkSecurityException(e, sys)


## =============================================================

## Data Validation Testing
# import sys

# from network_security.components.data_ingestion import DataIngestion
# from network_security.components.data_validation import DataValidation
# from network_security.entity.config_entity import (
#     DataIngestionConfig,
#     DataValidationConfig,
#     TrainingPipelineConfig,
# )
# from network_security.exception.exception import NetworkSecurityException
# from network_security.logging.logger import logging

# if __name__ == "__main__":
#     try:
#         training_pipeline_config = TrainingPipelineConfig()
#         data_ingestion_config = DataIngestionConfig(
#             training_pipeline_config=training_pipeline_config,
#         )
#         data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
#         logging.info("Initiated data ingestion")
#         data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
#         logging.info("Data Initiation Completed")
#         print(data_ingestion_artifact)

#         data_validation_config = DataValidationConfig(
#             training_pipeline_config=training_pipeline_config,
#         )
#         data_validation = DataValidation(
#             data_ingestion_artifact=data_ingestion_artifact,
#             data_validation_config=data_validation_config,
#         )
#         logging.info("Initiated data validation")
#         data_validation_artifact = data_validation.initiate_data_validation()
#         logging.info("Data Validation Completed")
#         print(data_validation_artifact)

#     except Exception as e:
#         raise NetworkSecurityException(e, sys)


## =============================================================

## Data Ingestion Testing

# import sys

# from network_security.components.data_ingestion import DataIngestion
# from network_security.entity.config_entity import (
#     DataIngestionConfig,
#     TrainingPipelineConfig,
# )
# from network_security.exception.exception import NetworkSecurityException
# from network_security.logging.logger import logging

# if __name__ == "__main__":
#     try:
#         training_pipeline_config = TrainingPipelineConfig()
#         data_ingestion_config = DataIngestionConfig(
#             training_pipeline_config=training_pipeline_config,
#         )
#         data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
#         logging.info("Initiated data ingestion")
#         data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
#         print(data_ingestion_artifact)
#     except Exception as e:
#         raise NetworkSecurityException(e, sys)

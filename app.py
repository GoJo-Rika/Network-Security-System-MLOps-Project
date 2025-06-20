import os
import sys
from urllib.parse import quote_plus

import certifi
import pymongo
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

from network_security.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.utils.main_utils.utils import load_object
from network_security.utils.ml_utils.model.estimator import NetworkModel

ca = certifi.where()


load_dotenv()
username = os.getenv("MONGO_DB_USERNAME")
password = os.getenv("MONGO_DB_PASSWORD")

username = quote_plus(username)
password = quote_plus(password)

mongo_db_url: str = f"mongodb+srv://{username}:{password}@cluster0.l5ee6dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_db_url, server_api=ServerApi("1"))

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)


database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route() -> Response:
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)

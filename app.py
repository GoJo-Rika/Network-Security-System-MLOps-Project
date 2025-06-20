import os
import sys
from pathlib import Path
from typing import Annotated
from urllib.parse import quote_plus

import certifi
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse
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
username = quote_plus(os.getenv("MONGO_DB_USERNAME"))
password = quote_plus(os.getenv("MONGO_DB_PASSWORD"))

mongo_db_url: str = f"mongodb+srv://{username}:{password}@cluster0.l5ee6dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_db_url, server_api=ServerApi("1"), tlsCAFile=ca)


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


@app.post("/predict")
async def predict_route(request: Request, file: Annotated[UploadFile, File()] = ...) -> _TemplateResponse:
    try:
        df = pd.read_csv(file.file)
        # print(df)
        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor, model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df["predicted_column"] = y_pred
        print(df["predicted_column"])
        # df['predicted_column'].replace(-1, 0)
        # return df.to_json()
        Path("prediction_output").mkdir(exist_ok=True)
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes="table table-striped")
        # print(table_html)
        return templates.TemplateResponse(
            "table.html", {"request": request, "table": table_html},
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8080)

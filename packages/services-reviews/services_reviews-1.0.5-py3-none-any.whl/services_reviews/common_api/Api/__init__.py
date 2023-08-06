"""Общий API сервис"""
from fastapi import FastAPI
from fastapi_restful import Api
from fastapi_sqlalchemy import db
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from services_reviews.common_configs import COMMON_API_CONFIG_DIR, DB_CONFIG_DIR
from services_reviews.common_utils.read_conf import ReadConf


conf_common_api = ReadConf.read("common_api", COMMON_API_CONFIG_DIR)
conf_db = ReadConf.read("db", DB_CONFIG_DIR)

APIv1 = conf_common_api.get('fastapi', 'APIV1')

CommonApi = FastAPI(title=__name__,
                    openapi_url=APIv1 + "/openapi.json",
                    docs_url=APIv1 + '/docs',
                    redoc_url=APIv1 + '/redoc',
                    swagger_ui_oauth2_redirect_url=APIv1 + "/docs/oauth2-redirect")

# CORS в продакшине надо изменить!
CommonApi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)

CommonApi.add_middleware(
    DBSessionMiddleware,
    db_url=f"postgresql+psycopg2://{conf_db.get('db','user')}:{conf_db.get('db','password')}@{conf_db.get('db','HOST')}:{conf_db.get('db','PORT')}/{conf_db.get('db','database')}"
)

api = Api(CommonApi)
from .common_controller import *
from .auth_controller import *
from .exceptions import *
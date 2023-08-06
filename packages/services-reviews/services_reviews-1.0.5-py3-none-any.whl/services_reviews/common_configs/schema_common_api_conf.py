#pylint: disable=no-name-in-module
from pydantic import BaseModel


class CommonApiConf(BaseModel):
    class FastAPIConf(BaseModel):
        csrf_enabled: bool
        secret_key: str
        jwt_secret_key: str
        jwt_storage: str
        debug: bool
        host: str # надо добавить регулярку
        port: int
        apiv1: str 
    fastapi: FastAPIConf

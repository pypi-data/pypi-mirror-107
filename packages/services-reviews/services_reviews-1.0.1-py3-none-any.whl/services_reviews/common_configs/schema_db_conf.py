#pylint: disable=no-name-in-module
from pydantic import BaseModel


class DBConf(BaseModel):
    class dbConf(BaseModel):
        host: str # надо добавить регулярку
        port: int
        database: str
        user: str
        password: str
    db: dbConf
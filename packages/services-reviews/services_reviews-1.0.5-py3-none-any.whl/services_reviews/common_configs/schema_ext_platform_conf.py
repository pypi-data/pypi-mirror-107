#pylint: disable=no-name-in-module
from pydantic import BaseModel, Field


class ExtPlatformConf(BaseModel):
    class DoubleGisConf(BaseModel):
        root_url: str
        api_key: str
        limit: int

    class YandexMapsConf(BaseModel):
        url_yandex_maps: str
        url_fetch_reviews: str
        yandex_uid_hardcode: str
        session_id_hardcode: str

    dobleGis: DoubleGisConf = Field(alias='2gis')
    yandexMaps: YandexMapsConf = Field(alias='yandexMaps')
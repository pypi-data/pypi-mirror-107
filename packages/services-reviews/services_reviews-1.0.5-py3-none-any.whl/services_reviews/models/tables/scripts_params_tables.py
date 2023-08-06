from services_reviews.models.base import Base
from services_reviews.models.mixins import OutputMixin
from sqlalchemy import Column, Integer, String, DateTime


class ParamsSendingRequestReview(OutputMixin, Base):
    """ Таблица с параметрами скрипта отправки отзывов """
    __tablename__ = 'params_sending_request_review'
    branch_id = Column(Integer,primary_key=True)
    frequency = Column(String(200))
    start_time_sending = Column(DateTime(timezone=True))


class ParamsApiRequestReview(OutputMixin, Base):
    """ Таблица с параметрами скрипта отправки отзывов """
    __tablename__ = 'params_api_request_review'
    record_id = Column(Integer, primary_key=True)
    frequency = Column(String(200))
    start_time_sending = Column(DateTime(timezone=True))
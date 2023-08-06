from services_reviews.models.base import Base
from services_reviews.models.mixins import OutputMixin
from sqlalchemy import Column, Integer, String, BIGINT, Boolean
from sqlalchemy.dialects import postgresql

class BranchesRef(OutputMixin, Base):
    """ таблица с информацией о конкретном филиале компании """
    __tablename__ = 'branches_ref'
    branch_id = Column(BIGINT, primary_key=True)
    branch_id_2gis = Column(BIGINT)
    branch_id_tripadvidor = Column(BIGINT)
    branch_id_yandexmap = Column(BIGINT)
    branch_name = Column(String(128), nullable=False)
    branch_address = Column(String(250))
    message_template = Column(String(250), nullable=False)
    is_parsing = Column(Boolean)

class PlatformRef(OutputMixin, Base):
    """ табличка id платформ """
    __tablename__ = 'platform_ref'
    platform_id = Column(Integer, primary_key=True)
    platform_name = Column(String(120))

class Companies(OutputMixin, Base):
    """ Таблица с компаниями """
    __tablename__ = 'companies'
    company_id = Column(BIGINT, primary_key=True)
    array_branch_id = Column(postgresql.ARRAY(BIGINT))
    company_name = Column(String(128))
    company_address = Column(String(250))


class BranchesFormData(OutputMixin, Base):
    """ Таблица с кастомизированными полями для формочек """
    __tablename__ = 'branches_form_data'
    branch_id = Column(BIGINT, primary_key=True)
    page_id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    subtitle_first = Column(String(1000))
    subtitle_second = Column(String(1000))
    recall_title = Column(String(1000))
    payload_data = Column(postgresql.ARRAY(String(120)))

class BranchesPlatformLink(OutputMixin, Base):
    """ Таблица с ссылками на платформы с формой отзыва для компании """
    __tablename__ = 'branches_platform_link'
    branch_id = Column(BIGINT, primary_key=True)
    platform_id = Column(Integer, primary_key=True)
    branch_link = Column(String(250))

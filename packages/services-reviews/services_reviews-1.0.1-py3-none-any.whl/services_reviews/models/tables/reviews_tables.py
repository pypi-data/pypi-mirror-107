from services_reviews.models.base import Base
from services_reviews.models.mixins import OutputMixin
from sqlalchemy import Column, ForeignKeyConstraint, ForeignKey, Integer, String, DateTime, Boolean, Float, Index, BIGINT

class DoubleGisReviews(OutputMixin, Base):
    """ Таблица с отдельными отзывами филиалов компаний от 2gis """
    __tablename__ = '2gis_reviews'

    branch_id_2gis = Column(BIGINT, primary_key=True)
    review_id = Column(BIGINT, primary_key=True)

    date_created = Column(DateTime(timezone=True))
    rating = Column(Integer)
    text = Column(String(2500))
    is_rated = Column(Boolean)
    likes = Column(Integer)
    user_id_2gis = Column(String(128))
    user_name_2gis = Column(String(128),nullable=True)


class BranchesDoubleGisReview(OutputMixin, Base):
    """ Таблица с рейтингом филиалов компаний от 2gis """
    __tablename__ = 'branches_2gis_review'
    record_id = Column(BIGINT, primary_key=True, autoincrement=True)
    branch_id_2gis = Column(BIGINT)
    DATE = Column(DateTime(timezone=True))

    org_reviews_count = Column(Integer)
    org_rating = Column(Float, nullable=True)
    branch_rating = Column(Float)
    branch_reviews_count = Column(Integer)

    __table_args__ = (
        Index('branch_id_2gis_DATE_idx', branch_id_2gis,
              DATE, postgresql_using='BTREE',unique=True),
    )


class YandexReviews(OutputMixin, Base):
    """ Таблица с отдельными отзывами филиалов компаний от Yandex """
    __tablename__ = 'yandex_reviews'
    branch_id_yandex = Column(BIGINT, primary_key=True)
    review_id = Column(BIGINT, primary_key=True)
    review_yandex_id = Column(String(60))
    date_created = Column(DateTime(timezone=True))
    rating = Column(Integer)
    text = Column(String(2500))
    user_name_yandex = Column(String(150),nullable=True)
    likes = Column(Integer)
    dislikes = Column(Integer)


    __table_args__ = (
        Index('branch_id_yandex_review_yandex_id_idx', branch_id_yandex,
              review_yandex_id, postgresql_using='BTREE', unique=True),
    )

class BranchYandexReview(OutputMixin, Base):
    """ Таблица с рейтингом филиалов компаний от Yandex """
    __tablename__ = 'branches_yandex_review'
    record_id = Column(Integer, primary_key=True)
    branch_id_yandex = Column(BIGINT)
    DATE = Column(DateTime(timezone=True))
    org_reviews_count = Column(BIGINT)
    org_rating = Column(Float, nullable=True)
    branch_rating = Column(Float, nullable=True)
    branch_reviews_count = Column(Integer)

    __table_args__ = (
        Index('branch_id_yandex_DATE_idx', branch_id_yandex,
              DATE, postgresql_using='BTREE',unique=True),
    )


class ServiceReview(OutputMixin, Base):
    """ наша внутренняя таблица с сервисом отзывов """
    __tablename__ = 'service_review'
    branch_id = Column(Integer, primary_key=True)
    request_id = Column(Integer, primary_key=True)
    review_id = Column(Integer, primary_key=True)
    text = Column(String(2500))
    date_created = Column(DateTime(timezone=True))
    rating = Column(Integer)
    platform_id = Column(Integer, ForeignKey('platform_ref.platform_id',ondelete='CASCADE'))

    __table_args__ = (
        ForeignKeyConstraint([branch_id, request_id],
                                ['review_requests.branch_id',
                                 'review_requests.request_id'],
                                ondelete="CASCADE"),
    )


class CommonBranchesReview(OutputMixin, Base):
    """ Общая таблица с рейтингом филиалов компаний """
    __tablename__ = 'common_branches_review'
    record_id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platform_ref.platform_id',ondelete='CASCADE'))
    branch_id = Column(Integer, ForeignKey('branches_ref.branch_id',ondelete='CASCADE'))
    date = Column(DateTime(timezone=True))
    org_reviews_count = Column(Integer)
    org_rating = Column(Float, nullable=True)
    branch_rating = Column(Float)
    branch_reviews_count = Column(Integer)

    __table_args__ = (
        Index('branch_id_platform_id_DATE_idx', branch_id, platform_id,
              date, postgresql_using='BTREE',unique=True),
    )


class CommonReviews(OutputMixin, Base):
    """ Общая таблица с рейтингом филиалов компаний """
    __tablename__ = 'common_reviews'
    platform_id = Column(Integer, ForeignKey('platform_ref.platform_id',ondelete='CASCADE'), primary_key=True)
    branch_id = Column(Integer, primary_key=True)
    review_id = Column(BIGINT, primary_key=True)
    date_created = Column(DateTime(timezone=True))
    rating = Column(Integer)
    text = Column(String(2500))
    user_id = Column(Integer)
    user_name = Column(String(128),nullable=True)

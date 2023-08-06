import enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum

from services_reviews.models.base import Base
from services_reviews.models.mixins import OutputMixin


class RequestStatus(enum.Enum):
    NEW = enum.auto()               # новый необработанный запрос
    ERROR_SENDING = enum.auto()     # ошибка во время отправки сообщения
    SENT = enum.auto()              # сообщение отправлено
    LINK_USED = enum.auto()         # совершён переход по ссылке
    COMPLETED = enum.auto()         # отзыв получен
    PURCHASE_EXPIRED = enum.auto()  # прошло много времени после покупки, а сообщение так и не отправлено
    REQUEST_EXPIRED = enum.auto()   # прошло много времени после отправки сообщения, а отзыв так и не получен


class ReviewStatus(enum.Enum):
    UNDEFINED = enum.auto()
    BAD = enum.auto()
    GOOD = enum.auto()

class ReviewRequests(OutputMixin, Base):
    """
    Табличка с запросами на ревью.
    Здесь имя/эмейл и т.д. не входят в первичный ключ - при новом заказе от того же человека
    (например, с тем же номером телефона) отсылаем ему новый запрос.
    """
    __tablename__ = 'review_requests'
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey('branches_ref.branch_id', ondelete='CASCADE'), primary_key=True)
    user_id_2gis = Column(Integer)
    user_id_yandex = Column(Integer)
    fio = Column(String(250), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(20))
    request_status = Column(Enum(RequestStatus), nullable=False, server_default=RequestStatus.NEW.name)
    review_status = Column(Enum(ReviewStatus), nullable=False, server_default=ReviewStatus.UNDEFINED.name)
    short_url = Column(String(200), index=True)
    stars = Column(Integer)
    text = Column(String(500))
    answer = Column(String(100))
    following_platform_link = Column(String(120))
    last_time_purchase = Column(DateTime(timezone=True))
    last_time_review_request = Column(DateTime(timezone=True))

    def __init__(self, branch_id, phone = '', name = ''):
        self.branch_id = branch_id
        self.phone = phone
        self.fio = name
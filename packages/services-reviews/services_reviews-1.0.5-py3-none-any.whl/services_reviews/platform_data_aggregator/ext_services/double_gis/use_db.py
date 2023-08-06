import datetime

from .dataclasses import ResponseReviewsDoubleGis
from services_reviews.common_utils.db_connect import dbConnector as dbc
from services_reviews.models import BranchesDoubleGisReview, DoubleGisReviews, BranchesRef


def get_branches_id_double_gis():
    """ получаем id филиалов 2gis-а """
    branch_id_2gis_query = dbc.session.query(BranchesRef.branch_id_2gis,BranchesRef.is_parsing).all()
    return branch_id_2gis_query

def send_data_double_gis_to_db(branch_id: int, resp: ResponseReviewsDoubleGis):
    """ Отправка данных с отзывами в базу """

    for review in resp.reviews:
        # сделать безопасный int()
        dbc.session.merge(
            DoubleGisReviews(
                branch_id_2gis = int(review.object.id),
                review_id = int(review.id),
                date_created = review.date_created,
                rating = review.rating,
                text = review.text,
                is_rated = review.is_rated,
                user_id_2gis = review.user.id,
                user_name_2gis = review.user.first_name,
                likes = review.likes_count
            )
        )

    dbc.session.add(
        BranchesDoubleGisReview(
            branch_id_2gis = branch_id,
            DATE = datetime.datetime.now(),
            org_reviews_count = resp.meta.org_reviews_count,
            org_rating = resp.meta.org_rating,
            branch_rating = resp.meta.branch_rating,
            branch_reviews_count = resp.meta.branch_reviews_count
        )
    )

    dbc.session.commit()
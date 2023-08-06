from .parser.routines import generate_s
from .dataclasses import ResponseReviewsYandex
from services_reviews.common_utils.db_connect import dbConnector as dbc
from services_reviews.models import YandexReviews, BranchesRef


def get_branches_id_yandex():
    """ получаем id филиалов yandex-a """
    branch_id_yandexmap_query = dbc.session.query(BranchesRef.branch_id_yandexmap, BranchesRef.is_parsing).all()
    return branch_id_yandexmap_query


def send_data_yandexmaps_to_db(branch_id: int, resp: ResponseReviewsYandex):
    """ Отправка данных с отзывами в базу """

    for review in resp.data.reviews:
        # сделать безопасный int()
        dbc.session.merge(
            YandexReviews(
                branch_id_yandex = int(review.businessId),
                review_id = generate_s(review.reviewId),
                review_yandex_id = review.reviewId,
                date_created = review.updatedTime,
                rating = review.rating,
                text = review.text,
                user_name_yandex = review.author.name if review.author is not None else None,
                likes = review.reactions.likes,
                dislikes = review.reactions.dislikes
            )
        )

    dbc.session.commit()

def call_update_branches_yandex_review():
    dbc.session.execute("SELECT public.update_branches_yandex_review()")
    dbc.session.commit()
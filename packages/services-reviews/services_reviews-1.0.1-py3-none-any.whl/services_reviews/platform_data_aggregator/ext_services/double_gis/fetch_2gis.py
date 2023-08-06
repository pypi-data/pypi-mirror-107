from .dataclasses import ResponseReviewsDoubleGis
from services_reviews.common_utils.read_conf import ReadConf
from services_reviews.common_utils import fetch


def get_2gis_reviews(company_id,link=None):
    """ получаем отзывы с 2gis """

    if link is not None:
        res = fetch.get(link)
        return res

    ROOT_URL = ReadConf.get("ES", "2gis", 'ROOT_URL')
    API_KEY = ReadConf.get("ES", "2gis", 'API_KEY')
    LIMIT = ReadConf.get("ES", "2gis", 'LIMIT')

    local_url = f"/branches/{company_id}/reviews"
    FULL_URL = ROOT_URL + local_url

    params = {
        'key': API_KEY,
        'limit': LIMIT,
        'rated': 'true',
        'sort_by': 'date_edited',
        'fields': 'meta.org_reviews_count,meta.org_rating,meta.branch_rating,meta.branch_reviews_count'
    }

    res = fetch.get(FULL_URL, params)
    return res


def parse_2gis_reviews_get_response(resp):
    reviews_2gis = ResponseReviewsDoubleGis.parse_raw(resp)
    return reviews_2gis
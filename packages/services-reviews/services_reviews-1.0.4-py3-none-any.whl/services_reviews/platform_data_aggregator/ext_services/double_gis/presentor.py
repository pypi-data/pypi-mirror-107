from services_reviews.platform_data_aggregator.ext_services.double_gis.fetch_2gis import get_2gis_reviews, parse_2gis_reviews_get_response
from services_reviews.platform_data_aggregator.ext_services.double_gis.use_db import send_data_double_gis_to_db, get_branches_id_double_gis

def insert_2gis_data():
    """ добавление данных от 2gis """
    for obj_branch in get_branches_id_double_gis():
        if obj_branch.is_parsing:
            recursive_next_link(obj_branch.branch_id_2gis)


def recursive_next_link(branch_id_2gis,link=None):
    """ рекурсивный обход по ссылкам """
    reviews_2gis = fetch_double_gis_row(branch_id_2gis,link)
    next_link = reviews_2gis.meta.next_link 
    if next_link is not None:
        recursive_next_link(branch_id_2gis, next_link)


def fetch_double_gis_row(branch_id_2gis,link = None):
    """ добавляем один снепшот данных запроса """
    if link is not None:
        res = get_2gis_reviews(branch_id_2gis, link)
    else:
        res = get_2gis_reviews(branch_id_2gis)
    reviews_2gis = parse_2gis_reviews_get_response(res)
    send_data_double_gis_to_db(branch_id_2gis, reviews_2gis)
    return reviews_2gis



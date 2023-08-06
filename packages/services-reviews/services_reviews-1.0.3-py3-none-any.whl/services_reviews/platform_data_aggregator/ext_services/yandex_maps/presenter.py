
from .parser.parsing_yandex_maps import parser_yandex
from .use_db import get_branches_id_yandex, send_data_yandexmaps_to_db, call_update_branches_yandex_review
from .dataclasses import ResponseReviewsYandex

def insert_yandexmaps_data():
    """ добавление данных yandex map """
    for obj_branch in get_branches_id_yandex():
        if obj_branch.is_parsing and obj_branch.branch_id_yandexmap is not None:
            loop_page_parsing(obj_branch.branch_id_yandexmap)
    call_update_branches_yandex_review()




def loop_page_parsing(businessId):
    """ цикл по страницам """
    page = 1
    totalPages = set_sample_data_page(businessId, page)
    page = 2
    while page < totalPages:
        totalPages = set_sample_data_page(businessId, page)
        if totalPages == -1:
            break
        page += 1


def set_sample_data_page(businessId, page):
    """ заполняем данные с одной страницы отзывов """
    res_json, totalPages = parser_yandex(businessId, page)
    if totalPages != -1:
        reviews_yandexmaps = parsing_yandex_data_row(res_json)
        send_data_yandexmaps_to_db(businessId, reviews_yandexmaps)
    return totalPages


def parsing_yandex_data_row(res):
    """ валидируем данные с запроса """
    try:
        reviews_yandexmaps = ResponseReviewsYandex.parse_obj(res)
    except:
        reviews_yandexmaps = None
        raise
    return reviews_yandexmaps

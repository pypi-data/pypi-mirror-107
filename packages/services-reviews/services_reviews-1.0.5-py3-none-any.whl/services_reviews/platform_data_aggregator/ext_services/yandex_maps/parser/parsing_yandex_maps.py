import re
import requests, logging
from services_reviews.platform_data_aggregator.ext_services.yandex_maps.parser.routines import generate_s_by_params
from services_reviews.common_utils.read_conf import ReadConf



def set_consts():
    global URL_YANDEX_MAPS, URL_FETCH_REVIEWS
    URL_YANDEX_MAPS =  ReadConf.get("ES", "yandexMaps", 'URL_YANDEX_MAPS')
    global URL_FETCH_REVIEWS
    URL_FETCH_REVIEWS = ReadConf.get("ES", "yandexMaps", 'URL_FETCH_REVIEWS')   

    global CSRF_TOKEN_KEY, S_KEY, YANDEX_UID_KEY, SESSION_ID_KEY
    CSRF_TOKEN_KEY = 'csrfToken'
    S_KEY = 's'
    YANDEX_UID_KEY = 'yandexuid'
    SESSION_ID_KEY = 'sessionId'

    global YANDEX_UID_HARDCODE, SESSION_ID_HARDCODE
    # хардкод авторизации (todo: избавиться)
    YANDEX_UID_HARDCODE = ReadConf.get("ES", "yandexMaps", 'YANDEX_UID_HARDCODE')
    SESSION_ID_HARDCODE = ReadConf.get("ES", "yandexMaps", 'SESSION_ID_HARDCODE')



def get_yandex_maps():
    """
    При повторных запусках скрипта Яндекс рисует капчу.
    Если открыть/обновить эту же страницу в браузере, и потом снова запустить скрипт - капчи не будет.
    UPD: теперь и после запроса в браузере всё равно при запросе через Питон вылазиет капча.
    todo? отловить запрос нажатия на галку и попробовать его отправлять автоматически?
    """
    headers = {
        # параметры скопированы из браузера
        'authority': 'yandex.ru',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
    }
    r = requests.get(URL_YANDEX_MAPS, headers=headers)
    if r.history:
        #print('Яндекс просит нажать галку :(')
        return YANDEX_UID_HARDCODE, SESSION_ID_HARDCODE

    cookies = r.cookies.get_dict()
    yandex_uid = cookies.get(YANDEX_UID_KEY, None)

    session_id = None
    m = re.search(r'"sessionId":"(\w+)"', r.text)
    if m is not None:
        session_id = m.group(1)
    return yandex_uid, session_id


def get_reviews(params, cookies):
    if S_KEY in params:
        del params[S_KEY]
    s = generate_s_by_params(params)
    params[S_KEY] = s

    r = requests.get(URL_FETCH_REVIEWS, params=params, cookies=cookies)

    return r


def parser_yandex(businessId, page, pageSize = 50):
    set_consts()
    yandex_uid, session_id = get_yandex_maps()
    if yandex_uid is None or session_id is None:
        #print(f'Error! {YANDEX_UID_KEY} is {yandex_uid}, {SESSION_ID_KEY} is {session_id}')
        return

    params = {
        'ajax': 1,
        'page': page,
        'pageSize': pageSize,  # если задать больше, то возвращается ошибка 500 Internal error
        'ranking': 'by_relevance_org',
        'sessionId': session_id,
        'businessId': businessId,
    }

    cookies = {
        'yandexuid': yandex_uid
    }

    r = get_reviews(params, cookies)
    if CSRF_TOKEN_KEY in r.json():
        params[CSRF_TOKEN_KEY] = r.json()[CSRF_TOKEN_KEY]
        r = get_reviews(params, cookies)

    if r.status_code == 200:
        result_json = r.json()
    else:
        logging.info(r.status_code)
        logging.info(r.text)
        return {}, -1

    # нужна проверка что приходит правильный джейсон
    try:
        totalPages = result_json['data']['params']['totalPages'] 
    except KeyError:
        raise

    return result_json, totalPages

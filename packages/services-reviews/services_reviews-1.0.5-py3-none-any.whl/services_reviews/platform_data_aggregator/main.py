import logging
from services_reviews.common_utils.read_conf import ReadConf
from services_reviews.common_utils.db_connect import dbConnector as dbc
from services_reviews.platform_data_aggregator.ext_services.double_gis.presentor import insert_2gis_data
from services_reviews.platform_data_aggregator.ext_services.yandex_maps.presenter import insert_yandexmaps_data
from services_reviews.common_configs import DB_CONFIG_DIR, EXT_PLATFORM_CONFIG_DIR

logging.basicConfig(level=logging.INFO)


def platform_data_aggregator():
    """ точка входа для запуска скрипта - агрегатора данных с внешних платформ """

    logging.info("Подгружаем конфигурационные файлы")
    ReadConf.read("ES", EXT_PLATFORM_CONFIG_DIR)
    ReadConf.read("db", DB_CONFIG_DIR)

    try:
        logging.info("Подключаемся к БД")
        dbc.start_connect_db()

        logging.info("Берем данные из 2gis и кладем в базу")
        insert_2gis_data()

        logging.info("Берем данные из Yandex Maps и кладем в базу")
        insert_yandexmaps_data()

        logging.info("Обновляем данные в общих таблицах")
        dbc.session.execute("SELECT public.update_common_reviews()")
        dbc.session.commit()
    finally:
        logging.info('finish')
        dbc.disconnect()

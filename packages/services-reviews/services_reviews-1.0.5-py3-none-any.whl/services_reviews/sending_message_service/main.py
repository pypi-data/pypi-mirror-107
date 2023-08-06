import logging
import time
from services_reviews.common_configs import DB_CONFIG_DIR, MESSAGE_SENDER_CONFIG_DIR, MessageSenderConf
from services_reviews.common_utils.db_connect import dbConnector as dbc
from services_reviews.common_utils.read_conf import ReadConf
from services_reviews.sending_message_service.message_service import MessageService
logging.basicConfig(level=logging.INFO)



def sending_message_service() -> None:
    """ скрипт для отправки запросов на отзвывы """

    # todo: unit test
    message_sender_conf: MessageSenderConf = ReadConf.read_parsed(MESSAGE_SENDER_CONFIG_DIR)
    ReadConf.read('db', DB_CONFIG_DIR)

    message_service = MessageService(message_sender_conf)

    while True:

        try:
            logging.info('Connecting to database')
            dbc.start_connect_db()

            logging.info('Preparing and sending messages')
            message_service.prepare_and_send_messages()

            logging.info('Saving changes')
            dbc.session.commit()

        finally:
            dbc.disconnect()

        logging.info('Completed successfully, loading for next session...')
        time.sleep(120)

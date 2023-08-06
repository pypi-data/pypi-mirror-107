import logging

import services_reviews.sending_message_service.messages.smsc.smsc_api as smsc_api
from services_reviews.common_configs import MessageSenderConf

logging.basicConfig(level=logging.INFO)


class ApiClientFacade:
    """ Фасад для работы с апи сервисов по отправке сообщений. """

    def __init__(self, config: MessageSenderConf):
        self._smsc = smsc_api.SMSC()

        smsc_api.SMSC_LOGIN = config.smsc.login
        smsc_api.SMSC_PASSWORD = config.smsc.api_password
        smsc_api.SMSC_DEBUG = config.smsc.debug

        self.COST_THRESHOLD = config.message_sender.max_message_cost

    def send_message(self, phone: str, message: str) -> bool:
        balance = float(self._smsc.get_balance())
        cost, _ = self._smsc.get_sms_cost(phone, message)
        print(balance, cost)
        cost = float(cost)
        if cost > balance:
            logging.error(f'Balance is {balance}, cost is {cost}. We need more money!')
            return False
        if cost > self.COST_THRESHOLD:
            logging.warning(f'Cost is {cost}, but threshold is {self.COST_THRESHOLD}. Too expensive message, skip it.')
            return False

        print(f"{phone}, {message}")
        _, _, final_cost, _ = self._smsc.send_sms(phone, message)
        print(final_cost)
        final_cost = float(final_cost)
        if final_cost != cost:
            logging.warning(f'Something went wrong: preparing cost was {cost}, but final cost is {final_cost}. '
                            f'Need to check at smsc.ru.')
        return True

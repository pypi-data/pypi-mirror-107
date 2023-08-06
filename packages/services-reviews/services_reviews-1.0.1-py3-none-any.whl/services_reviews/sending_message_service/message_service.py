import logging
import secrets
import string

from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from services_reviews.common_configs import MessageSenderConf
from services_reviews.models.tables.review_requests_tables import RequestStatus, ReviewRequests
from services_reviews.sending_message_service.exceptions import SendingMessageException, \
    UnknownTemplateVariableException
from services_reviews.sending_message_service.message_crud import get_new_requests, get_template, get_branch_name, \
    is_link_unique
from services_reviews.sending_message_service.messages.api_client_facade import ApiClientFacade

logging.basicConfig(level=logging.INFO)


class MessageService(object):

    def __init__(self, config: MessageSenderConf):
        self.api_facade = ApiClientFacade(config)

        self.LINK_ALPHABET: str = string.ascii_letters + string.digits
        self.LINK_SIZE = config.message_sender.link_size
        self.URL_TEMPLATE = config.message_sender.short_url_template

    def prepare_and_send_messages(self) -> None:
        """ Get new requests, prepare messages and send them. """
        for request in get_new_requests():
            logging.info(f'Processing phone number {request.phone}...')
            self.generate_link(request)
            logging.debug(f'Generated or retrieved link is {request.short_url}')
            try:
                message = self.get_message(request)
                logging.debug(f'Generated message is:\n{message}')
            except (SendingMessageException, NoResultFound, MultipleResultsFound) as e:
                logging.warning(f'An error occurred: {e}. Skip phone number {request.phone}')
                request.request_status = RequestStatus.ERROR_SENDING
            else:
                self.send_and_handle_status(request, message)
            logging.debug(f'Request status is {request.request_status}')

    def generate_link(self, request: ReviewRequests) -> None:
        """ Generate unique link and save it to review request if there's no link yet. """
        if request.short_url is not None:
            return
        while True:
            link = ''.join(secrets.choice(self.LINK_ALPHABET) for _ in range(self.LINK_SIZE))
            if is_link_unique(link):
                break
        request.short_url = link

    def get_message(self, request: ReviewRequests) -> str:
        """ Construct message with review request. """
        branch_name = get_branch_name(request.branch_id)
        template = get_template(request.branch_id)
        try:
            message = template.format(branch_name=branch_name, fio=request.fio,
                                      link=self.link_to_url(request.short_url))
        except KeyError as e:
            raise UnknownTemplateVariableException(f"Unknown template variable: {repr(e.args[0])}") from None
        return message

    def link_to_url(self, link: str) -> str:
        """ Create https url from link postfix """
        return self.URL_TEMPLATE.format(link)

    def send_and_handle_status(self, request: ReviewRequests, message: str) -> None:
        """ Send message and save status in DB. """
        status = self.api_facade.send_message(request.phone, message)
        if status:
            request.request_status = RequestStatus.SENT
        else:
            request.request_status = RequestStatus.ERROR_SENDING

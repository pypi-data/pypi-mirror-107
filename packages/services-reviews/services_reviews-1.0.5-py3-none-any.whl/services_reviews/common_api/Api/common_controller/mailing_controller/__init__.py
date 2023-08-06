from services_reviews.common_api.Api import api, APIv1
from .mailing_resources import MailingSender

api.add_resource(MailingSender(), APIv1 + '/mailing/send')
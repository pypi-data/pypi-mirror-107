from services_reviews.common_api.Api import api, APIv1
from .system_resources import Heartbeat
from .form_controller import *
from .mailing_controller import *

api.add_resource(Heartbeat(),APIv1 + '/heartbeat')
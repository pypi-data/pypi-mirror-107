from services_reviews.common_api.Api import api, APIv1
from .form_resources import RaitingStars, FeedbackData, PlatformLinkFollow
from .form_render_resources import RenderPages, RenderLinks

api.add_resource(RaitingStars(), APIv1 + '/form/stars')
api.add_resource(FeedbackData(), APIv1 + '/form/feedback')
api.add_resource(PlatformLinkFollow(), APIv1 + '/form/typelink')

api.add_resource(RenderPages(), APIv1 + '/form/text')
api.add_resource(RenderLinks(), APIv1 + '/form/linklists')
from services_reviews.common_api.Api import api, APIv1
from .auth_resources import UserLogin, RefreshAccessToken, UserRegistration, UserLogout, UserInfo, CheckToken

api.add_resource(UserLogin(), APIv1 + '/login')
api.add_resource(RefreshAccessToken(), APIv1 + '/refresh')
api.add_resource(UserRegistration(), APIv1 + '/registration')
api.add_resource(UserLogout(), APIv1 + '/logout')
api.add_resource(CheckToken(), APIv1 + '/check-token')
api.add_resource(UserInfo(), APIv1 + '/user/{id}')

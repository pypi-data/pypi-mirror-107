# pylint: disable=no-name-in-module
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from services_reviews.common_api.Api import conf_common_api


class RegistrationUser(BaseModel):
    username: str
    password: str
    branchId: int 

class RequestUser(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = conf_common_api.get('fastapi', 'JWT_SECRET_KEY')
    authjwt_token_location: set = {conf_common_api.get('fastapi', 'JWT_STORAGE')}
    authjwt_cookie_csrf_protect: bool = True


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RegistrationResponse(BaseModel):
    msg: str


class LogoutResponse(BaseModel):
    msg: str


class RefreshTokenResponse(BaseModel):
    access_token: str


class ErrorResponse(BaseModel):
    detail: str

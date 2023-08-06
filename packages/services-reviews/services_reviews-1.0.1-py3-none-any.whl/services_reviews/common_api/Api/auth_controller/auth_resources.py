from fastapi import HTTPException, Depends, Request
from services_reviews.common_api.Api import CommonApi, db
from functools import wraps
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_restful import Resource, set_responses
from fastapi_jwt_auth.exceptions import AuthJWTException
from .dataclases import RequestUser, AuthJWT, LoginResponse, RegistrationResponse, LogoutResponse, RefreshTokenResponse, ErrorResponse
from services_reviews.models import User
from .crud import save_to_db, add_token_to_blacklist, is_jti_blacklisted


@CommonApi.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


class UserRegistration(Resource):
    @set_responses(
        RegistrationResponse,
        200,
        {
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, user: RequestUser, authorize: AuthJWT = Depends()):
        new_user = User(username=user.username, password=User.generate_hash(user.password))

        try:
            if save_to_db(new_user):
                return JSONResponse(status_code=200, content=RegistrationResponse(msg=f"User {user.username} was created").dict())
            else:
                return JSONResponse(status_code=200, content=RegistrationResponse(msg=f"User {user.username} already exist").dict())
        except:
            raise HTTPException(status_code=500, detail="Something went wrong")


class UserLogin(Resource):
    @set_responses(
        LoginResponse,
        200,
        {
            401: {
                "model": ErrorResponse
            },
            406: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, user: RequestUser, authorize: AuthJWT = Depends()):
        current_user = db.session.query(User).filter_by(username=user.username).first()
        if current_user is not None:
            if User.verify_hash(user.password, current_user.password):
                access_token = authorize.create_access_token(subject=user.username)
                refresh_token = authorize.create_refresh_token(subject=user.username)
                return JSONResponse(status_code=200, content=LoginResponse(access_token=access_token, refresh_token=refresh_token).dict())
            else:
                raise HTTPException(status_code=401, detail="Invalid password")
        else:
            raise HTTPException(status_code=406, detail="User not found")


class UserLogout(Resource):
    @set_responses(
        LogoutResponse,
        200,
        {
            500: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, authorize: AuthJWT = Depends()):
        authorize.jwt_required()

        jti = authorize.get_raw_jwt()['jti']
        try:
            add_token_to_blacklist(jti)
            return JSONResponse(status_code=200, content=LogoutResponse(msg='Access token has been revoked').dict())
        except:
            raise HTTPException(status_code=500, detail='Something went wrong')


class RefreshAccessToken(Resource):
    @set_responses(
        RefreshTokenResponse,
        200,
        {
            401: {
                "model": ErrorResponse
            },
            422: {
                "model": ErrorResponse
            }
        }
    )
    def post(self, authorize: AuthJWT = Depends()):
        authorize.jwt_refresh_token_required()
        jti = authorize.get_raw_jwt()['jti']

        if is_jti_blacklisted(jti):
            raise HTTPException(status_code=401, detail='Token revoked')

        current_user = authorize.get_jwt_subject()
        access_token = authorize.create_access_token(subject=current_user)
        return JSONResponse(status_code=200, content=RefreshTokenResponse(access_token=access_token).dict())


class CheckToken(Resource):
    @set_responses(
        None,
        200,
        {
            401: {
                "model": ErrorResponse
            }
        }
    )
    def get(self, authorize: AuthJWT = Depends()):
        authorize.jwt_required()
        jti = authorize.get_raw_jwt()['jti']
        if is_jti_blacklisted(jti):
            raise HTTPException(status_code=401, detail='Token revoked')
        return JSONResponse(status_code=200, content=None)


def jwt_required(func):
    @wraps(func)
    def wrapper(authorize: AuthJWT = Depends(), *args, **kw):
        authorize.jwt_refresh_token_required()
        jti = authorize.get_raw_jwt()['jti']

        if is_jti_blacklisted(jti):
            raise HTTPException(status_code=401, detail='Token revoked')

        return func(*args, **kw)
    return wrapper


class UserInfo(Resource):
    @jwt_required
    def get(self, id: int, authorize: AuthJWT = Depends()):
        return id

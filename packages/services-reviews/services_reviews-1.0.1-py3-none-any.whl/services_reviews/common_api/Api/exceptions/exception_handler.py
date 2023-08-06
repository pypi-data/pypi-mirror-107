from fastapi import Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from services_reviews.common_api.Api import CommonApi, db
from services_reviews.common_api.Api.routines import JSONErrorResponse
from fastapi.exceptions import RequestValidationError, RequestErrorModel
from services_reviews.common_api.Api.exceptions import HTTPCommonException


@CommonApi.exception_handler(AuthJWTException)
async def authjwt_exception_handler(request: Request,exc: AuthJWTException):
    return JSONErrorResponse(
        status_code=exc.status_code,
        text= exc.message
    )

@CommonApi.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msg = exc.errors()[0]['msg']
    if msg == 'field required':
        msg = f"Требуется следующее поле: {exc.errors()[0]['loc'][1]}"
    return JSONErrorResponse(status_code=400, text=msg)


@CommonApi.exception_handler(500)
async def bad_request_exception_handler(request: Request, exc: RequestErrorModel):
    return JSONErrorResponse(status_code=500, text="Что-то пошло не так")

@CommonApi.exception_handler(HTTPCommonException)
async def common_exception_handler(request: Request, exc: HTTPCommonException):
    return JSONErrorResponse(status_code=exc.status_code, text=exc.message)


from typing import Tuple
from fastapi.responses import JSONResponse
from .dataclasses import ErrorResponse, Error, StatusResponse


def error_types_responses(*codes: Tuple):
    return { k: { "model": ErrorResponse } for k in codes }

def get_error_response(text: str):
    return ErrorResponse(error=Error(text=text)).dict()

def JSONErrorResponse(status_code: int, text: str):
    return JSONResponse(status_code=status_code, content=get_error_response(text=text))

def JSONOKResponse():
    JSONResponse(status_code=200, content=StatusResponse(status=0).dict())
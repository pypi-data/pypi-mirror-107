from pydantic import BaseModel

class Error(BaseModel):
    text: str

class ErrorResponse(BaseModel):
    error: Error


class StatusResponse(BaseModel):
    status: int

from pydantic import BaseModel


class MailingDataRequest(BaseModel):
    phone: str
    name: str
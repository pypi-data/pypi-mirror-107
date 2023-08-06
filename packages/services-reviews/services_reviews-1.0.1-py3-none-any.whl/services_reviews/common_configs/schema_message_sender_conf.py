from pydantic import BaseModel


class MessageSenderConf(BaseModel):
    class SmscConf(BaseModel):
        login: str
        api_password: str
        debug: bool

    class SenderConf(BaseModel):
        short_url_base: str
        short_url_template: str
        link_size: int
        max_message_cost: int

    smsc: SmscConf
    message_sender: SenderConf

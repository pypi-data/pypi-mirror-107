# pylint: disable=no-name-in-module
from pydantic import BaseModel
from typing import Optional, List, Dict


class DataRaitngRequests(BaseModel):
    count: int
    hashId: str


class FeedbackDataRequests(BaseModel):
    hashId: str
    text: str
    answer: str

class PlarformLinkRequests(BaseModel):
    platformName: str
    hashId: str

class RecallAnswerTypes(BaseModel):
    answerTypeFirst: str
    answerTypeSecond: str

class FormTextDataResponses(BaseModel):
    nameCompany: str
    title: Optional[str]
    subtitleFirst: Optional[str]
    subtitleSecond: Optional[str]
    recallTitle: Optional[str]
    recallAnswerTypes: Optional[RecallAnswerTypes]


class FormLinkDataResponses(BaseModel):
    payload: Dict[str,str]

#pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
from typing import Optional, List


class ResponseReviewsDoubleGis(BaseModel):
    class Meta(BaseModel):
        code: int
        next_link: Optional[str]
        branch_rating: float
        branch_reviews_count: int
        org_rating: float
        org_reviews_count: int

    class Review(BaseModel):
        class Object(BaseModel):
            id: str
            type: str

        class User(BaseModel):
            class PhotoPreview(BaseModel):
                big_size: Optional[str] = Field(alias="1920x")
                av_size: Optional[str] = Field(alias="320x")

            id: str
            reviews_count: int
            first_name: Optional[str]
            latest_name: Optional[str]
            name: str
            provider: str
            photo_preview_urls: Optional[PhotoPreview]
            url: Optional[str]

        class OfficalAnswer(BaseModel):
            id: str
            org_name: str
            text: str
            date_created: str

        id: str
        region_id: int
        text: str
        rating: int
        provider: str
        is_hidden: bool
        hiding_type: Optional[str]
        hiding_reason: Optional[str]
        url: str
        likes_count: int
        comments_count: int
        date_created: str
        date_edited: Optional[str]
        object: Object
        user: User
        official_answer: Optional[OfficalAnswer]
        on_moderation: bool
        is_rated: bool

    meta: Meta
    reviews: List[Review]
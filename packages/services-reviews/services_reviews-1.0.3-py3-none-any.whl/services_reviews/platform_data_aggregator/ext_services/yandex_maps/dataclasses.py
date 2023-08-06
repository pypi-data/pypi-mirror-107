#pylint: disable=no-name-in-module
from pydantic import BaseModel
from typing import Optional, List, Any

from pydantic.fields import Field


class ResponseReviewsYandex(BaseModel):
    class Data(BaseModel):
        class Review(BaseModel):
            class Author(BaseModel):
                name: str
                profileUrl: str
                avatarUrl: str
                professionLevel: str

            class Reactions(BaseModel):
                likes: int
                dislikes: int
                userReaction: str

            reviewId: str
            businessId: str
            author: Optional[Author]
            text: str
            rating: int
            updatedTime: str
            hasComments: bool
            reactions: Reactions
            photos : Optional[List[Any]]
        
        class Params(BaseModel):
            offset: int
            limit: int
            count: int
            loadedReviewsCount: Optional[int]
            page: int
            totalPages: int
            reviewsRemained: int

        reviews: List[Review]
        params: Params
        tags: List[str]

    data: Data
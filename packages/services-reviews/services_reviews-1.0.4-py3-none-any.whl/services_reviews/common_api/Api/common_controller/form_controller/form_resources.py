from fastapi_restful import Resource
from .dataclasses import DataRaitngRequests, FeedbackDataRequests, PlarformLinkRequests
from services_reviews.common_api.Api import db
from services_reviews.models import ReviewRequests, RequestStatus, ReviewStatus
from services_reviews.common_api.Api.routines import JSONOKResponse
from services_reviews.common_api.Api.exceptions import HTTPCommonException

class RaitingStars(Resource):
    def post(self, data_stars: DataRaitngRequests):
        current_request = db.session.query(ReviewRequests).filter_by(short_url=data_stars.hashId).first()
        if current_request is None:
            raise HTTPCommonException(404, message="Bad hash")

        if current_request.request_status in (RequestStatus.COMPLETED, RequestStatus.PURCHASE_EXPIRED, RequestStatus.REQUEST_EXPIRED):
            raise HTTPCommonException(406, message="Link already approved")
        
        current_request.stars = data_stars.count

        db.session.merge(current_request)
        db.session.commit()

        return JSONOKResponse()

class FeedbackData(Resource):
    def post(self, data_feedback: FeedbackDataRequests):
        current_request = db.session.query(ReviewRequests).filter_by(short_url=data_feedback.hashId).first()
        if current_request is None:
            raise HTTPCommonException(404, message="Bad hash")        

        if current_request.request_status in (RequestStatus.COMPLETED, RequestStatus.PURCHASE_EXPIRED, RequestStatus.REQUEST_EXPIRED):
            raise HTTPCommonException(406, message="Link already approved")

        current_request.request_status = RequestStatus.COMPLETED
        current_request.review_status = ReviewStatus.BAD
        current_request.text = data_feedback.text
        current_request.answer = data_feedback.answer

        db.session.merge(current_request)
        db.session.commit()

        return JSONOKResponse()


class PlatformLinkFollow(Resource):
    def post(self, data_platform_link: PlarformLinkRequests):
        current_request = db.session.query(ReviewRequests).filter_by(short_url=data_platform_link.hashId).first()
        if current_request is None:
            raise HTTPCommonException(404, message="Bad hash")        

        if current_request.request_status in (RequestStatus.COMPLETED, RequestStatus.PURCHASE_EXPIRED, RequestStatus.REQUEST_EXPIRED):
            raise HTTPCommonException(406, message="Link already approved")

        current_request.request_status = RequestStatus.COMPLETED
        current_request.review_status = ReviewStatus.GOOD
        current_request.following_platform_link = data_platform_link.platformName

        db.session.merge(current_request)
        db.session.commit()

        return JSONOKResponse()
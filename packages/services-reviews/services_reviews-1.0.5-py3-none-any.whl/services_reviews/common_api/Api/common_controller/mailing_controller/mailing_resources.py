from fastapi import Depends
from fastapi_restful import Resource
from fastapi_jwt_auth import AuthJWT
from .dataclasses import MailingDataRequest
from services_reviews.common_api.Api import db
from services_reviews.models import ReviewRequests, User
from services_reviews.common_api.Api.routines import JSONOKResponse
from services_reviews.common_api.Api.exceptions import HTTPCommonException
from services_reviews.common_api.Api.auth_controller.auth_resources import jwt_required

class MailingSender(Resource):
    @jwt_required
    def post(self, data: MailingDataRequest, authorize: AuthJWT = Depends()):
        current_user = authorize.get_jwt_subject()
        user = db.session.query(User).filter_by(username = current_user).first()
        if user is None:
            raise HTTPCommonException(406, message="User not found")

        rewiew_request = ReviewRequests(branch_id = user.branch_id, phone = data.phone, name = data.name)
        db.session.add(rewiew_request)
        db.session.commit()
        
        return JSONOKResponse()
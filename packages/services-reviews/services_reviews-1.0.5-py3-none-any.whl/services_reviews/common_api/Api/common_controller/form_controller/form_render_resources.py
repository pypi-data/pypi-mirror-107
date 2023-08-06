from fastapi_restful import Resource
from fastapi.responses import JSONResponse
from .dataclasses import FormTextDataResponses, RecallAnswerTypes, FormLinkDataResponses
from services_reviews.common_api.Api import db
from services_reviews.common_api.Api.exceptions import HTTPCommonException
from services_reviews.models import ReviewRequests, BranchesRef, BranchesFormData, BranchesPlatformLink, PlatformRef

class RenderPages(Resource):
    def get(self, hashId: str, pageId: int):
        """ возвращаем текстовое описание страницы """
        current_request = db.session.query(ReviewRequests).filter_by(short_url=hashId).first() 
        if current_request is None:
            raise HTTPCommonException(404, message="Bad hash")     

        branch = db.session.query(BranchesRef).filter_by(branch_id=current_request.branch_id).first() 
        if branch is None:
            raise HTTPCommonException(404, message="Company not found")   
        
        branch_form_data = db.session.query(BranchesFormData).filter_by(branch_id=current_request.branch_id, page_id=pageId).first() 
        if branch_form_data is None:
            return JSONResponse(status_code=200, content=FormTextDataResponses(
                     nameCompany = branch.branch_name
                  ).dict())

        recall_answer_types = None
        if branch_form_data.payload_data is not None:
            if len(branch_form_data.payload_data) > 1:
                recall_answer_types = RecallAnswerTypes(answerTypeFirst=branch_form_data.payload_data[0], answerTypeSecond=branch_form_data.payload_data[1])

        response = FormTextDataResponses(
            nameCompany = branch.branch_name,
            title = branch_form_data.title,
            subtitleFirst = branch_form_data.subtitle_first,
            subtitleSecond = branch_form_data.subtitle_second,
            recallTitle = branch_form_data.recall_title,
            recallAnswerTypes = recall_answer_types
        )

        return JSONResponse(status_code=200, content=response.dict())



class RenderLinks(Resource):
    def get(self, hashId: str):
        """ возвращаем список ссылок на платформы """
        current_request = db.session.query(ReviewRequests).filter_by(short_url=hashId).first() 
        if current_request is None:
            raise HTTPCommonException(404, message="Bad hash")     
        
        dict_links = {}

        for platform_link, platform in db.session.query(BranchesPlatformLink, PlatformRef)\
            .filter(BranchesPlatformLink.platform_id == PlatformRef.platform_id)\
            .filter(BranchesPlatformLink.branch_id == current_request.branch_id)\
            .all():
            dict_links[platform.platform_name] = platform_link.branch_link
        
        response = FormLinkDataResponses(payload=dict_links)
        return JSONResponse(status_code=200, content=response.dict())
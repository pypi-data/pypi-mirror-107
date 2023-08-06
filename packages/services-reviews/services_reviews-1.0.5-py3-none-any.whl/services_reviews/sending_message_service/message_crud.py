from typing import Iterable

from services_reviews.common_utils.db_connect import dbConnector as dbc
from services_reviews.models import ReviewRequests, BranchesRef
from services_reviews.models.tables.review_requests_tables import RequestStatus


def get_new_requests() -> Iterable[ReviewRequests]:
    """ Get new review requests to send """
    recipients_query = dbc.session.query(ReviewRequests)\
        .where(ReviewRequests.request_status.in_((RequestStatus.NEW, RequestStatus.ERROR_SENDING)))\
        .limit(100)     # todo: use limit and offset in loop
    return recipients_query


def get_branch_name(branch_id: int) -> str:
    """ Get branch name by branch id """
    branch_name = dbc.session.query(BranchesRef.branch_name).where(BranchesRef.branch_id == branch_id).one()
    return branch_name[0]


def get_template(branch_id: int) -> str:
    """ Get branch template message by branch id """
    template = dbc.session.query(BranchesRef.message_template).where(BranchesRef.branch_id == branch_id).one()
    return template[0]


def is_link_unique(link: str) -> bool:
    """
    Check if this link already contains in review requests.
    Return True if not contains, return False if contains.
    """
    return dbc.session.query(ReviewRequests).where(ReviewRequests.short_url == link).count() == 0

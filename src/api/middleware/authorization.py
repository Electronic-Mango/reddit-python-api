"""
Module holding middleware blueprint used for API requests authorization.
"""

from logging import getLogger
from flask import abort, Blueprint, request

from settings import API_AUTHORIZATION_HEADER_NAME, API_AUTHORIZATION_HEADER_VALUE

blueprint = Blueprint("authorization", __name__)


@blueprint.before_app_request
def authorize_request() -> None:
    """Authorize app requests based on a authorization header from settings.yml"""
    if not API_AUTHORIZATION_HEADER_NAME or not API_AUTHORIZATION_HEADER_VALUE:
        getLogger("waitress").info("Authorization disabled")
        return
    auth_header_value = request.headers.get(API_AUTHORIZATION_HEADER_NAME)
    if auth_header_value != API_AUTHORIZATION_HEADER_VALUE:
        getLogger("waitress").info(f"Authorization failed, received value: [{auth_header_value}]")
        abort(401, "Authorization header value doesn't match expected one")

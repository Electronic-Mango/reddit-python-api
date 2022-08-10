"""
Module holding middleware blueprint logging every API request.
"""

from logging import getLogger

from flask import Blueprint, request

blueprint = Blueprint("before_request", __name__)


@blueprint.before_app_request
def log_request() -> None:
    """Log all app requests"""
    getLogger("waitress").info(request)

"""
Module holding blueprint firing before each app request.
This blueprint is used for logging each request.
"""

from logging import getLogger

from flask import Blueprint, request

blueprint = Blueprint("before_request", __name__)


@blueprint.before_app_request
def log_request():
    """Log all app requests"""
    getLogger("waitress").info(request)

"""
Blueprint of API endpoint returning a random submission from a user.
"""

from typing import Any

from flask import Blueprint

from api.responses import prepare_random_response
from reddit.reddit import get_user_submissions
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("user/submission/random", __name__)

@blueprint.route("/user/submission/random/<username>")
@blueprint.route("/user/submission/random/<username>/<int:load_count>")
@blueprint.route("/user/submission/random/<username>/<int:load_count>/<sort>")
def user_random_submission(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a random submission from the given user

    Up to "load_count" submissions are loaded from user, then a random one is selected.
    Number of loaded submissions can be lower if user has fewer submissions.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random submission from given user.
    """
    return prepare_random_response(username, load_count, sort, get_user_submissions)

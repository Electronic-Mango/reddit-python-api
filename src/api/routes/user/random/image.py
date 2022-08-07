"""
Blueprint of API endpoint returning a random image submission from a user.
"""

from typing import Any

from flask import Blueprint

from api.prepare_response import prepare_random_response
from reddit.reddit import get_user_image_submissions
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("user/image/random", __name__)

@blueprint.route("/user/image/random/<username>")
@blueprint.route("/user/image/random/<username>/<int:load_count>")
@blueprint.route("/user/image/random/<username>/<int:load_count>/<sort>")
def user_random_image_submission(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a random image submission (image, GIF) from the given user

    Up to "load_count" image submissions are loaded from user, then a random one is selected.
    Number of loaded submissions can be lower if user has fewer submissions and due to filtering
    only image submissions from the loaded ones.
    Still, the higher the "load_count" the lower the chance of returning the same submission
    on repeated calls.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random image submission from given user.
    """
    return prepare_random_response(username, load_count, sort, get_user_image_submissions)

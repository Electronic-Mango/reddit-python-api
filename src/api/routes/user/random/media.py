"""
Blueprint of API endpoint returning a random media submission from a user.
"""

from typing import Any

from flask import Blueprint

from api.prepare_response import prepare_random_response
from reddit.client import get_user_image_submissions
from reddit.wrapper import SortType
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("user/media/random", __name__)


@blueprint.route("/user/media/random/<username>")
@blueprint.route("/user/media/random/<username>/<int:load_count>")
@blueprint.route("/user/media/random/<username>/<int:load_count>/<sort:sort>")
async def user_random_image_submission(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: SortType = SortType.hot,
) -> dict[str, Any]:
    """Endpoint returning a random media submission (media, GIF) from the given user

    Up to "load_count" media submissions are loaded from user, then a random one is selected.
    Number of loaded submissions can be lower if user has fewer submissions and due to filtering
    only media submissions from the loaded ones.
    Still, the higher the "load_count" the lower the chance of returning the same submission
    on repeated calls.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (SortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random media submission from given user.
    """
    return await prepare_random_response(username, load_count, sort, get_user_image_submissions)

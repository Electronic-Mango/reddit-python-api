"""
Blueprint of API endpoint returning a list of submissions for a user.
"""

from typing import Any

from flask import Blueprint

from api.prepare_response import prepare_list_response_or_abort
from api.reddit_client import get_user_submissions
from reddit.wrapper import SortType
from settings import DEFAULT_LOAD_COUNT

blueprint = Blueprint("/user/submission", __name__)


@blueprint.route("/user/submission/<username>")
@blueprint.route("/user/submission/<username>/<int:load_count>")
@blueprint.route("/user/submission/<username>/<int:load_count>/<sort:sort>")
async def user_submissions(
    username: str,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: SortType = SortType.hot,
) -> dict[str, Any]:
    """Endpoint returning a list of submissions from the given user

    Argument "load_count" specifies only how many submissions are loaded from user.
    Final count of submissions can be lower than "load_count" argument if given user has fewer
    submissions.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (SortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded submissions and total submission count
    """
    submissions = await get_user_submissions(username, load_count, sort)
    return prepare_list_response_or_abort(submissions)

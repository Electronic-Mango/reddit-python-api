"""
Blueprint of API endpoint returning a random submission from a subreddit.
"""

from typing import Any

from flask import Blueprint

from api.routes.prepare_response import prepare_random_response_or_abort
from reddit.client import get_subreddit_submissions
from reddit.wrapper import SortType
from settings import DEFAULT_LOAD_COUNT, DEFAULT_SUBREDDIT

blueprint = Blueprint("/subreddit/submission/random", __name__)


@blueprint.route("/subreddit/submission/random")
@blueprint.route("/subreddit/submission/random/<subreddit>")
@blueprint.route("/subreddit/submission/random/<subreddit>/<int:load_count>")
@blueprint.route("/subreddit/submission/random/<subreddit>/<int:load_count>/<sort:sort>")
async def subreddit_random_submission(
    subreddit: str = DEFAULT_SUBREDDIT,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: SortType = SortType.hot,
) -> dict[str, Any]:
    """Endpoint returning a random submission from the given subreddit

    Up to "load_count" submissions are loaded from subreddit, then a random one is selected.
    Number of loaded submissions can be lower if subreddit has fewer submissions.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (SortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random submission from given subreddit.
    """
    submissions = await get_subreddit_submissions(subreddit, load_count, sort)
    return prepare_random_response_or_abort(submissions)

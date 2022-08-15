"""
Blueprint of API endpoint returning a list of submissions for a subreddit.
"""

from typing import Any

from flask import Blueprint

from api.reddit_client import get_subreddit_submissions
from api.routes.prepare_response import prepare_list_response_or_abort
from reddit.wrapper import SortType
from settings import DEFAULT_LOAD_COUNT, DEFAULT_SUBREDDIT

blueprint = Blueprint("/subreddit/submission", __name__)


@blueprint.route("/subreddit/submission")
@blueprint.route("/subreddit/submission/<subreddit>")
@blueprint.route("/subreddit/submission/<subreddit>/<int:load_count>")
@blueprint.route("/subreddit/submission/<subreddit>/<int:load_count>/<sort:sort>")
async def subreddit_submissions(
    subreddit: str = DEFAULT_SUBREDDIT,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: SortType = SortType.hot,
) -> dict[str, Any]:
    """Endpoint returning a list of submissions from the given subreddit

    Argument "load_count" specifies only how many submissions are loaded from subreddit.
    Final count of submissions can be lower than "load_count" argument if given subreddit has fewer
    submissions.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (SortType, optional): "hot", "top", "new", "controversial".
                                   Defaults to "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded submissions and total submission count.
    """
    submissions = await get_subreddit_submissions(subreddit, load_count, sort)
    return prepare_list_response_or_abort(submissions)

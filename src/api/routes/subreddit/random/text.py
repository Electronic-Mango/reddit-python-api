"""
Blueprint of API endpoint returning a random text submission from a subreddit.
"""

from typing import Any

from flask import Blueprint

from api.prepare_response import prepare_random_response
from reddit.client import get_subreddit_text_submissions
from settings import DEFAULT_LOAD_COUNT, DEFAULT_SUBREDDIT

blueprint = Blueprint("/subreddit/text/random", __name__)


@blueprint.route("/subreddit/text/random")
@blueprint.route("/subreddit/text/random/<subreddit>")
@blueprint.route("/subreddit/text/random/<subreddit>/<int:load_count>")
@blueprint.route("/subreddit/text/random/<subreddit>/<int:load_count>/<sort>")
def random_text_submission(
    subreddit: str = DEFAULT_SUBREDDIT,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a random text submission from the given subreddit

    Up to "load_count" text submissions are loaded from subreddit, then a random one is selected.
    Number of loaded submissions can be lower if subreddit has fewer submissions and due to
    filtering only text submissions from the loaded ones.
    Still, the higher the "load_count" the lower the chance of returning the same submission
    on repeated calls.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random text submission from given subreddit.
    """
    return prepare_random_response(subreddit, load_count, sort, get_subreddit_text_submissions)

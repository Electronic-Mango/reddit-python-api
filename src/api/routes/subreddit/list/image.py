"""
Blueprint of API endpoint returning a list of image submissions for a subreddit.
"""

from typing import Any

from flask import Blueprint

from api.prepare_response import prepare_list_response
from reddit.client import get_subreddit_image_submissions
from settings import DEFAULT_LOAD_COUNT, DEFAULT_SUBREDDIT

blueprint = Blueprint("/subreddit/image", __name__)

@blueprint.route("/subreddit/image")
@blueprint.route("/subreddit/image/<subreddit>")
@blueprint.route("/subreddit/image/<subreddit>/<int:load_count>")
@blueprint.route("/subreddit/image/<subreddit>/<int:load_count>/<sort>")
def image_submissions(
    subreddit: str = DEFAULT_SUBREDDIT,
    load_count: int = DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a list of image submissions (images, GIFs) from the given subreddit

    Argument "load_count" specifies only how many submissions are loaded from subreddit.
    Final count of submissions can be lower than "load_count" argument if given subreddit has fewer
    submissions and due to filtering only image submissions.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded image submissions and total submission count.
    """
    return prepare_list_response(subreddit, load_count, sort, get_subreddit_image_submissions)

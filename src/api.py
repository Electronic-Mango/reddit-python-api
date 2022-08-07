"""
Module responsible for API itself, holds all endpoint routes.
"""

from logging import INFO, basicConfig, getLogger
from os import getenv
from random import choice
from typing import Any, Callable

from dotenv import load_dotenv
from flask import abort, Flask, request
from waitress import serve

from reddit import (
    get_subreddit_media_submissions,
    get_subreddit_submissions,
    get_subreddit_text_submissions,
    get_user_media_submissions,
    get_user_submissions,
    get_user_text_submissions,
    jsonify_submission,
    Submission,
)

load_dotenv()
_API_HOST = getenv("API_HOST")
_API_PORT = getenv("API_PORT")
_DEFAULT_SUBREDDIT = getenv("DEFAULT_SUBREDDIT")
_DEFAULT_LOAD_COUNT = int(getenv("DEFAULT_LOAD_COUNT"))

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.before_request
def log_request():
    getLogger("waitress").info(request)


@app.route("/subreddit/submission")
@app.route("/subreddit/submission/<subreddit>")
@app.route("/subreddit/submission/<subreddit>/<int:load_count>")
@app.route("/subreddit/submission/<subreddit>/<int:load_count>/<sort>")
def submissions(
    subreddit: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
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
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded submissions and total submission count.
    """
    return _prepare_list_response(subreddit, load_count, sort, get_subreddit_submissions)


@app.route("/subreddit/media")
@app.route("/subreddit/media/<subreddit>")
@app.route("/subreddit/media/<subreddit>/<int:load_count>")
@app.route("/subreddit/media/<subreddit>/<int:load_count>/<sort>")
def media_submissions(
    subreddit: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a list of media submissions (images, GIFs) from the given subreddit

    Argument "load_count" specifies only how many submissions are loaded from subreddit.
    Final count of submissions can be lower than "load_count" argument if given subreddit has fewer
    submissions and due to filtering only media submissions.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded media submissions and total submission count.
    """
    return _prepare_list_response(subreddit, load_count, sort, get_subreddit_media_submissions)


@app.route("/subreddit/text")
@app.route("/subreddit/text/<subreddit>")
@app.route("/subreddit/text/<subreddit>/<int:load_count>")
@app.route("/subreddit/text/<subreddit>/<int:load_count>/<sort>")
def text_submissions(
    subreddit: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a list of text submissions from the given subreddit

    Argument "load_count" specifies only how many submissions are loaded from subreddit.
    Final count of submissions can be lower than "load_count" argument if given subreddit has fewer
    submissions and due to filtering only text submissions.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded text submissions and total submission count.
    """
    return _prepare_list_response(subreddit, load_count, sort, get_subreddit_text_submissions)


@app.route("/subreddit/submission/random")
@app.route("/subreddit/submission/random/<subreddit>")
@app.route("/subreddit/submission/random/<subreddit>/<int:load_count>")
@app.route("/subreddit/submission/random/<subreddit>/<int:load_count>/<sort>")
def random_submission(
    subreddit: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a random submission from the given subreddit

    Up to "load_count" submissions are loaded from subreddit, then a random one is selected.
    Number of loaded submissions can be lower if subreddit has fewer submissions.

    Args:
        subreddit (str, optional): subreddit to load data from.
                                   Defaults to DEFAULT_SUBREDDIT from .env.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random submission from given subreddit.
    """
    return _prepare_random_response(subreddit, load_count, sort, get_subreddit_submissions)


@app.route("/subreddit/media/random")
@app.route("/subreddit/media/random/<subreddit>")
@app.route("/subreddit/media/random/<subreddit>/<int:load_count>")
@app.route("/subreddit/media/random/<subreddit>/<int:load_count>/<sort>")
def random_media_submission(
    subreddit: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a random media submission (image, GIF) from the given subreddit

    Up to "load_count" media submissions are loaded from subreddit, then a random one is selected.
    Number of loaded submissions can be lower if subreddit has fewer submissions and due to
    filtering only media submissions from the loaded ones.
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
        dict[str, Any]: JSON storing data of one random media submission from given subreddit.
    """
    return _prepare_random_response(subreddit, load_count, sort, get_subreddit_media_submissions)


@app.route("/subreddit/text/random")
@app.route("/subreddit/text/random/<subreddit>")
@app.route("/subreddit/text/random/<subreddit>/<int:load_count>")
@app.route("/subreddit/text/random/<subreddit>/<int:load_count>/<sort>")
def random_text_submission(
    subreddit: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
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
    return _prepare_random_response(subreddit, load_count, sort, get_subreddit_text_submissions)


@app.route("/user/submission/<username>")
@app.route("/user/submission/<username>/<int:load_count>")
@app.route("/user/submission/<username>/<int:load_count>/<sort>")
def user_submissions(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a list of submissions from the given user

    Argument "load_count" specifies only how many submissions are loaded from user.
    Final count of submissions can be lower than "load_count" argument if given user has fewer
    submissions.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded submissions and total submission count
    """
    return _prepare_list_response(username, load_count, sort, get_user_submissions)


@app.route("/user/media/<username>")
@app.route("/user/media/<username>/<int:load_count>")
@app.route("/user/media/<username>/<int:load_count>/<sort>")
def user_media_submissions(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a list of media submissions (images, GIFs) from the given user

    Argument "load_count" specifies only how many submissions are loaded from user.
    Final count of submissions can be lower than "load_count" argument if given user has fewer
    submissions and due to filtering only media submissions.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded media submissions and total submission count.
    """
    return _prepare_list_response(username, load_count, sort, get_user_media_submissions)


@app.route("/user/text/<username>")
@app.route("/user/text/<username>/<int:load_count>")
@app.route("/user/text/<username>/<int:load_count>/<sort>")
def user_text_submissions(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a list of text submissions from the given user

    Argument "load_count" specifies only how many submissions are loaded from user.
    Final count of submissions can be lower than "load_count" argument if given user has fewer
    submissions and due to filtering only text submissions.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing list of loaded text submissions and total submission count.
    """
    return _prepare_list_response(username, load_count, sort, get_user_text_submissions)


@app.route("/user/submission/random/<username>")
@app.route("/user/submission/random/<username>/<int:load_count>")
@app.route("/user/submission/random/<username>/<int:load_count>/<sort>")
def user_random_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
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
    return _prepare_random_response(username, load_count, sort, get_user_submissions)


@app.route("/user/media/random/<username>")
@app.route("/user/media/random/<username>/<int:load_count>")
@app.route("/user/media/random/<username>/<int:load_count>/<sort>")
def user_random_media_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a random media submission (image, GIF) from the given user

    Up to "load_count" media submissions are loaded from user, then a random one is selected.
    Number of loaded submissions can be lower if user has fewer submissions and due to filtering
    only media submissions from the loaded ones.
    Still, the higher the "load_count" the lower the chance of returning the same submission
    on repeated calls.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random media submission from given user.
    """
    return _prepare_random_response(username, load_count, sort, get_user_media_submissions)


@app.route("/user/text/random/<username>")
@app.route("/user/text/random/<username>/<int:load_count>")
@app.route("/user/text/random/<username>/<int:load_count>/<sort>")
def user_random_text_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    """Endpoint returning a random text submission from the given user

    Up to "load_count" text submissions are loaded from user, then a random one is selected.
    Number of loaded submissions can be lower if user has fewer submissions and due to filtering
    only text submissions from the loaded ones.
    Still, the higher the "load_count" the lower the chance of returning the same submission
    on repeated calls.

    Args:
        username (str): user to load data from.
        load_count (int, optional): how many submissions should be loaded before one is selected.
                                    Defaults to DEFAULT_LOAD_COUNT from .env.
        sort (str, optional): "controversial", "top", "new", others are interpreted as "hot".
                              Defaults to None, which will be interpreter as "hot".

    Returns:
        dict[str, Any]: JSON storing data of one random text submission from given user.
    """
    return _prepare_random_response(username, load_count, sort, get_user_text_submissions)


def _prepare_list_response(
    source_name: str,
    load_count: int,
    sort: str,
    submissions_generator: Callable[[str, int], list[Submission]],
) -> dict[str, Any]:
    submissions = _get_submissions_or_abort(source_name, load_count, sort, submissions_generator)
    submissions = [jsonify_submission(submission) for submission in submissions]
    return {"count": len(submissions), "submissions": submissions}


def _prepare_random_response(
    source_name: str,
    load_count: int,
    sort: str,
    submissions_generator: Callable[[str, int, str], list[Submission]],
) -> dict[str, Any]:
    submissions = _get_submissions_or_abort(source_name, load_count, sort, submissions_generator)
    random_submission = choice(submissions)
    return jsonify_submission(random_submission)


def _get_submissions_or_abort(
    source_name: str,
    load_count: int,
    sort: str,
    submissions_generator: Callable[[str, int, str], list[Submission]],
) -> list[Submission]:
    submissions = submissions_generator(source_name, load_count, sort)
    if not submissions:
        abort(404, f"No entries found for {source_name}")
    return submissions


if __name__ == "__main__":
    basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=INFO)
    serve(app, host=_API_HOST, port=_API_PORT)

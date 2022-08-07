from logging import INFO, basicConfig, getLogger
from os import getenv
from random import choice
from typing import Any, Callable

from dotenv import load_dotenv
from flask import abort, Flask, request
from waitress import serve

from reddit import (
    get_media_submissions,
    get_submissions,
    get_text_submissions,
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


@app.route("/")
@app.route("/<subreddit_name>")
@app.route("/submission")
@app.route("/submission/<subreddit_name>")
@app.route("/submission/<subreddit_name>/<int:load_count>")
@app.route("/submission/<subreddit_name>/<int:load_count>/<sort>")
@app.route("/subreddit")
@app.route("/subreddit/submission")
@app.route("/subreddit/submission/<subreddit_name>")
@app.route("/subreddit/submission/<subreddit_name>/<int:load_count>")
@app.route("/subreddit/submission/<subreddit_name>/<int:load_count>/<sort>")
def submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, sort, get_submissions)


@app.route("/media")
@app.route("/media/<subreddit_name>")
@app.route("/media/<subreddit_name>/<int:load_count>")
@app.route("/media/<subreddit_name>/<int:load_count>/<sort>")
@app.route("/subreddit/media")
@app.route("/subreddit/media/<subreddit_name>")
@app.route("/subreddit/media/<subreddit_name>/<int:load_count>")
@app.route("/subreddit/media/<subreddit_name>/<int:load_count>/<sort>")
def media_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, sort, get_media_submissions)


@app.route("/text")
@app.route("/text/<subreddit_name>")
@app.route("/text/<subreddit_name>/<int:load_count>")
@app.route("/text/<subreddit_name>/<int:load_count>/<sort>")
@app.route("/subreddit/text")
@app.route("/subreddit/text/<subreddit_name>")
@app.route("/subreddit/text/<subreddit_name>/<int:load_count>")
@app.route("/subreddit/text/<subreddit_name>/<int:load_count>/<sort>")
def text_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, sort, get_text_submissions)


@app.route("/random")
@app.route("/random/<subreddit_name>")
@app.route("/random/submission/<subreddit_name>")
@app.route("/random/submission/<subreddit_name>/<int:load_count>")
@app.route("/random/submission/<subreddit_name>/<int:load_count>/<sort>")
@app.route("/subreddit/random")
@app.route("/subreddit/random/<subreddit_name>")
@app.route("/subreddit/random/submission/<subreddit_name>")
@app.route("/subreddit/random/submission/<subreddit_name>/<int:load_count>")
@app.route("/subreddit/random/submission/<subreddit_name>/<int:load_count>/<sort>")
def random_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, sort, get_submissions)


@app.route("/random/media")
@app.route("/random/media/<subreddit_name>")
@app.route("/random/media/<subreddit_name>/<int:load_count>")
@app.route("/random/media/<subreddit_name>/<int:load_count>/<sort>")
@app.route("/subreddit/random/media")
@app.route("/subreddit/random/media/<subreddit_name>")
@app.route("/subreddit/random/media/<subreddit_name>/<int:load_count>")
@app.route("/subreddit/random/media/<subreddit_name>/<int:load_count>/<sort>")
def random_media_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, sort, get_media_submissions)


@app.route("/random/text")
@app.route("/random/text/<subreddit_name>")
@app.route("/random/text/<subreddit_name>/<int:load_count>")
@app.route("/random/text/<subreddit_name>/<int:load_count>/<sort>")
@app.route("/subreddit/random/text")
@app.route("/subreddit/random/text/<subreddit_name>")
@app.route("/subreddit/random/text/<subreddit_name>/<int:load_count>")
@app.route("/subreddit/random/text/<subreddit_name>/<int:load_count>/<sort>")
def random_text_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, sort, get_text_submissions)


@app.route("/user/submission/<username>")
@app.route("/user/submission/<username>/<int:load_count>")
@app.route("/user/submission/<username>/<int:load_count>/<sort>")
def user_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_list_response(username, load_count, sort, get_user_submissions)


@app.route("/user/media/<username>")
@app.route("/user/media/<username>/<int:load_count>")
@app.route("/user/media/<username>/<int:load_count>/<sort>")
def user_media_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_list_response(username, load_count, sort, get_user_media_submissions)


@app.route("/user/text/<username>")
@app.route("/user/text/<username>/<int:load_count>")
@app.route("/user/text/<username>/<int:load_count>/<sort>")
def user_text_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_list_response(username, load_count, sort, get_user_text_submissions)


@app.route("/user/random/submission/<username>")
@app.route("/user/random/submission/<username>/<int:load_count>")
@app.route("/user/random/submission/<username>/<int:load_count>/<sort>")
def user_random_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_random_response(username, load_count, sort, get_user_submissions)


@app.route("/user/random/media/<username>")
@app.route("/user/random/media/<username>/<int:load_count>")
@app.route("/user/random/media/<username>/<int:load_count>/<sort>")
def user_random_media_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
    return _prepare_random_response(username, load_count, sort, get_user_media_submissions)


@app.route("/user/random/text/<username>")
@app.route("/user/random/text/<username>/<int:load_count>")
@app.route("/user/random/text/<username>/<int:load_count>/<sort>")
def user_random_text_submission(
    username: str,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: str = None,
) -> dict[str, Any]:
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

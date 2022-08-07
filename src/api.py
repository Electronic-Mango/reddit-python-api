from logging import INFO, basicConfig, getLogger
from os import getenv
from random import choice
from typing import Any, Callable

from dotenv import load_dotenv
from flask import abort, Flask, request
from waitress import serve
from werkzeug.routing import BaseConverter

from reddit import (
    get_media_submissions,
    get_submissions,
    get_text_submissions,
    jsonify_submission,
    SortType,
    Submission,
)

load_dotenv()
_API_HOST = getenv("API_HOST")
_API_PORT = getenv("API_PORT")
_DEFAULT_SUBREDDIT = getenv("DEFAULT_SUBREDDIT")
_DEFAULT_LOAD_COUNT = int(getenv("DEFAULT_LOAD_COUNT"))
_DEFAULT_SORT_TYPE = SortType.HOT


class SortTypeConverter(BaseConverter):
    def to_python(self, value: str) -> SortType:
        try:
            return SortType[value.upper()]
        except KeyError:
            return SortType.HOT

    def to_url(self, sort_type: SortType) -> str:
        return sort_type.name.lower()


app = Flask(__name__)
app.url_map.strict_slashes = False
app.url_map.converters["sort"] = SortTypeConverter


@app.before_request
def log_request():
    getLogger("waitress").info(request)


@app.route("/")
@app.route("/<subreddit_name>")
@app.route("/submission")
@app.route("/submission/<subreddit_name>")
@app.route("/submission/<subreddit_name>/<int:load_count>")
@app.route("/submission/<subreddit_name>/<int:load_count>/<sort:sort>")
def submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: SortType = _DEFAULT_SORT_TYPE,
) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, sort, get_submissions)


@app.route("/media")
@app.route("/media/<subreddit_name>")
@app.route("/media/<subreddit_name>/<int:load_count>")
@app.route("/media/<subreddit_name>/<int:load_count>/<sort:sort>")
def media_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: SortType = _DEFAULT_SORT_TYPE,
) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, sort, get_media_submissions)


@app.route("/text")
@app.route("/text/<subreddit_name>")
@app.route("/text/<subreddit_name>/<int:load_count>")
@app.route("/text/<subreddit_name>/<int:load_count>/<sort:sort>")
def text_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: SortType = _DEFAULT_SORT_TYPE,
) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, sort, get_text_submissions)


@app.route("/random")
@app.route("/random/<subreddit_name>")
@app.route("/random/submission/<subreddit_name>")
@app.route("/random/submission/<subreddit_name>/<int:load_count>")
@app.route("/random/submission/<subreddit_name>/<int:load_count>/<sort:sort>")
def random_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: SortType = _DEFAULT_SORT_TYPE,
) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, sort, get_submissions)


@app.route("/random/media")
@app.route("/random/media/<subreddit_name>")
@app.route("/random/media/<subreddit_name>/<int:load_count>")
@app.route("/random/media/<subreddit_name>/<int:load_count>/<sort:sort>")
def random_media_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: SortType = _DEFAULT_SORT_TYPE,
) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, sort, get_media_submissions)


@app.route("/random/text")
@app.route("/random/text/<subreddit_name>")
@app.route("/random/text/<subreddit_name>/<int:load_count>")
@app.route("/random/text/<subreddit_name>/<int:load_count>/<sort:sort>")
def random_text_submission(
    subreddit_name: str = _DEFAULT_SUBREDDIT,
    load_count: int = _DEFAULT_LOAD_COUNT,
    sort: SortType = _DEFAULT_SORT_TYPE,
) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, sort, get_text_submissions)


def _prepare_list_response(
    subreddit_name: str,
    load_count: int,
    sort: SortType,
    submissions_generator: Callable[[str, int], list[Submission]],
) -> dict[str, Any]:
    submissions = _get_submissions_or_abort(subreddit_name, load_count, sort, submissions_generator)
    submissions = [jsonify_submission(submission) for submission in submissions]
    return {"count": len(submissions), "submissions": submissions}


def _prepare_random_response(
    subreddit_name: str,
    load_count: int,
    sort: SortType,
    submissions_generator: Callable[[str, int, SortType], list[Submission]],
) -> dict[str, Any]:
    submissions = _get_submissions_or_abort(subreddit_name, load_count, sort, submissions_generator)
    random_submission = choice(submissions)
    return jsonify_submission(random_submission)


def _get_submissions_or_abort(
    subreddit_name: str,
    load_count: int,
    sort: SortType,
    submissions_generator: Callable[[str, int, SortType], list[Submission]],
) -> list[Submission]:
    submissions = submissions_generator(subreddit_name, load_count, sort)
    if not submissions:
        abort(404, f"No entries found for {subreddit_name}")
    return submissions


if __name__ == "__main__":
    basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=INFO)
    serve(app, host=_API_HOST, port=_API_PORT)

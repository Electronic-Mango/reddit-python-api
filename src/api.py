from datetime import datetime
from logging import INFO, basicConfig, getLogger
from os import getenv
from random import choice
from typing import Any, Callable

from dotenv import load_dotenv
from flask import abort, Flask, request
from waitress import serve

from reddit import get_media_submissions, get_submissions, get_text_submissions, Submission

load_dotenv()
_API_HOST = getenv("API_HOST")
_API_PORT = getenv("API_PORT")
_DEFAULT_LOAD_COUNT = int(getenv("DEFAULT_LOAD_COUNT"))

app = Flask(__name__)


@app.before_request
def log_request():
    getLogger("waitress").info(request)


@app.route("/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/submission/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/submission/<subreddit_name>/<int:load_count>")
def submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, get_submissions)


@app.route("/media/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/media/<subreddit_name>/<int:load_count>")
def media_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, get_media_submissions)


@app.route("/text/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/text/<subreddit_name>/<int:load_count>")
def text_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_list_response(subreddit_name, load_count, get_text_submissions)


@app.route("/random/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/random/submission/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/random/submission/<subreddit_name>/<int:load_count>")
def random_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, get_submissions)


@app.route("/random/media/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/random/media/<subreddit_name>/<int:load_count>")
def random_media_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, get_media_submissions)


@app.route("/random/text/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/random/text/<subreddit_name>/<int:load_count>")
def random_text_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_random_response(subreddit_name, load_count, get_text_submissions)


def _prepare_list_response(
    subreddit_name: str,
    load_count: int,
    submissions_generator: Callable[[str, int], list[Submission]],
) -> dict[str, Any]:
    submissions = _prepare_submissions_or_abort(subreddit_name, load_count, submissions_generator)
    submissions = [_jsonify_submission(submission) for submission in submissions]
    return {"count": len(submissions), "submissions": submissions}


def _prepare_random_response(
    subreddit_name: str,
    load_count: int,
    submissions_generator: Callable[[str, int], list[Submission]],
) -> dict[str, Any]:
    submissions = _prepare_submissions_or_abort(subreddit_name, load_count, submissions_generator)
    random_submission = choice(submissions)
    return _jsonify_submission(random_submission)


def _prepare_submissions_or_abort(
    subreddit_name: str,
    load_count: int,
    submissions_generator: Callable[[str, int], list[Submission]],
) -> list[Submission]:
    submissions = submissions_generator(subreddit_name, load_count)
    if not submissions:
        abort(404, f"No entries found for {subreddit_name}")
    return submissions


def _jsonify_submission(submission: Submission) -> dict[str, Any]:
    return {
        "id": submission.id,
        "url": submission.url,
        "title": submission.title,
        "author": submission.author.name,
        "nsfw": submission.over_18,
        "spoiler": submission.spoiler,
        "selftext": submission.selftext,
        "score": submission.score,
        "created_utc": datetime.utcfromtimestamp(submission.created_utc),
        "shortlink": submission.shortlink,
    }


if __name__ == "__main__":
    basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=INFO)
    app.url_map.strict_slashes = False
    serve(app, host=_API_HOST, port=_API_PORT)

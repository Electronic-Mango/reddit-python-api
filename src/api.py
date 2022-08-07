from logging import INFO, basicConfig, getLogger
from os import getenv
from typing import Any, Callable

from dotenv import load_dotenv
from flask import abort, Flask, request
from markupsafe import escape
from waitress import serve

from reddit import (
    get_random_media_submission,
    get_random_submission,
    get_random_text_submission,
    Submission,
)

load_dotenv()
_API_HOST = getenv("API_HOST")
_API_PORT = getenv("API_PORT")
_DEFAULT_LOAD_COUNT = int(getenv("DEFAULT_LOAD_COUNT"))

app = Flask(__name__)


@app.before_request
def log_request():
    getLogger("waitress").info(request)


@app.route("/submission/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/submission/<subreddit_name>/<int:load_count>")
def random_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_response(subreddit_name, load_count, get_random_submission)


@app.route("/media/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/media/<subreddit_name>/<int:load_count>")
def random_media_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_response(subreddit_name, load_count, get_random_media_submission)


@app.route("/text/<subreddit_name>", defaults={"load_count": _DEFAULT_LOAD_COUNT})
@app.route("/text/<subreddit_name>/<int:load_count>")
def random_text_submission(subreddit_name: str, load_count: int) -> dict[str, Any]:
    return _prepare_response(subreddit_name, load_count, get_random_text_submission)


def _prepare_response(
    subreddit_name: str, load_count: int, submission_generator: Callable[[str, int], Submission]
) -> dict[str, Any]:
    escaped_subreddit_name = escape(subreddit_name)
    submission = submission_generator(escaped_subreddit_name, load_count)
    if not submission:
        abort(404, f"No entries found for {escaped_subreddit_name}")
    return {
        "id": submission.id,
        "url": submission.url,
        "title": submission.title,
        "author": submission.author.name,
        "nsfw": submission.over_18,
        "spoiler": submission.spoiler,
        "selftext": submission.selftext,
    }


if __name__ == "__main__":
    basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=INFO)
    serve(app, host=_API_HOST, port=_API_PORT)

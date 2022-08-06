from typing import Any, Callable
from flask import abort, Flask
from markupsafe import escape

from reddit import (
    get_random_media_submission,
    get_random_submission,
    get_random_text_submission,
    Submission,
)

app = Flask(__name__)


@app.route("/submission/<subreddit_name>")
def random_submission(subreddit_name: str) -> dict[str, Any]:
    return _prepare_response(subreddit_name, get_random_submission)


@app.route("/media/<subreddit_name>")
def random_media_submission(subreddit_name: str) -> dict[str, Any]:
    return _prepare_response(subreddit_name, get_random_media_submission)


@app.route("/text/<subreddit_name>")
def random_text_submission(subreddit_name: str) -> dict[str, Any]:
    return _prepare_response(subreddit_name, get_random_text_submission)


def _prepare_response(
    subreddit_name: str, submission_generator: Callable[[str], Submission]
) -> dict[str, Any]:
    escaped_subreddit_name = escape(subreddit_name)
    submission = submission_generator(escaped_subreddit_name)
    if not submission:
        abort(404, f"No entries found for {escaped_subreddit_name}")
    return {
        "id": submission.id,
        "url": submission.url,
        "title": submission.title,
        "author": submission.author.name,
        "nsfw": submission.over_18,
        "spoiler": submission.spoiler,
        "text": submission.selftext_html,
    }

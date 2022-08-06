from flask import abort, Flask
from markupsafe import escape

from reddit import get_random_submission

app = Flask(__name__)


@app.route("/")
def hello():
    return "<p>Hello!</p>"


@app.route("/submission/<subreddit_name>")
def random_submission(subreddit_name: str):
    escaped_subreddit_name = escape(subreddit_name)
    submission = get_random_submission(escaped_subreddit_name)
    if not submission:
        abort(404, f"No entries found for {escaped_subreddit_name}")
    return {
        "id": submission.id,
        "url": submission.url,
        "title": submission.title,
        "author": submission.author.name,
        "nsfw": submission.over_18,
        "spoiler": submission.spoiler,
    }

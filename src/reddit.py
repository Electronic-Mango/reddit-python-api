from os import getenv
from random import choice

from dotenv import load_dotenv
from praw import Reddit
from praw.models import Submission
from prawcore import Redirect

load_dotenv()
_REDDIT_CLIENT_ID = getenv("REDDIT_CLIENT_ID")
_REDDIT_CLIENT_SECRET = getenv("REDDIT_CLIENT_SECRET")
_REDDIT_CLIENT_USER_AGENT = getenv("REDDIT_CLIENT_USER_AGENT")
_LOAD_COUNT = int(getenv("DEFAULT_LOAD_COUNT"))
_MEDIA_SUBMISSION_URL_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif")

_client = Reddit(
    client_id=_REDDIT_CLIENT_ID,
    client_secret=_REDDIT_CLIENT_SECRET,
    user_agent=_REDDIT_CLIENT_USER_AGENT,
)


def get_random_submission(subreddit: str, load_count: int = _LOAD_COUNT) -> Submission:
    submissions = _get_submissions(subreddit, load_count)
    return choice(submissions) if submissions else None


def get_random_media_submission(subreddit: str, load_count: int = _LOAD_COUNT) -> Submission:
    submissions = _get_submissions(subreddit, load_count)
    media_submissions = [
        submission for submission in submissions if _submission_is_media(submission)
    ]
    return choice(media_submissions) if media_submissions else None


def _get_submissions(subreddit: str, load_count: int) -> list[Submission]:
    try:
        return list(_client.subreddit(subreddit).hot(limit=load_count))
    except Redirect:
        return []


def _submission_is_media(submission: Submission) -> bool:
    return submission.url.endswith(_MEDIA_SUBMISSION_URL_SUFFIXES)

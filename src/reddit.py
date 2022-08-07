from os import getenv
from typing import Callable

from dotenv import load_dotenv
from praw import Reddit
from praw.models import Submission
from prawcore import Redirect

load_dotenv()
_REDDIT_CLIENT_ID = getenv("REDDIT_CLIENT_ID")
_REDDIT_CLIENT_SECRET = getenv("REDDIT_CLIENT_SECRET")
_REDDIT_CLIENT_USER_AGENT = getenv("REDDIT_CLIENT_USER_AGENT")
_MEDIA_SUBMISSION_URL_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif")

_client = Reddit(
    client_id=_REDDIT_CLIENT_ID,
    client_secret=_REDDIT_CLIENT_SECRET,
    user_agent=_REDDIT_CLIENT_USER_AGENT,
)


def get_submissions(subreddit: str, load_count: int) -> list[Submission]:
    return _get_submissions_with_filtering(subreddit, load_count, lambda _: True)


def get_media_submissions(subreddit: str, load_count: int) -> list[Submission]:
    return _get_submissions_with_filtering(subreddit, load_count, _submission_is_media)


def get_text_submissions(subreddit: str, load_count: int) -> list[Submission]:
    return _get_submissions_with_filtering(subreddit, load_count, _submission_is_text)


def _get_submissions_with_filtering(
    subreddit: str, load_count: int, submission_filter: Callable[[Submission], bool]
) -> list[Submission]:
    submissions = _get_submissions(subreddit, load_count)
    return [submission for submission in submissions if submission_filter(submission)]


def _get_submissions(subreddit: str, load_count: int) -> list[Submission]:
    try:
        return list(_client.subreddit(subreddit).hot(limit=load_count))
    except Redirect:
        return []


def _submission_is_media(submission: Submission) -> bool:
    return submission.url.endswith(_MEDIA_SUBMISSION_URL_SUFFIXES)


def _submission_is_text(submission: Submission) -> bool:
    return submission.selftext_html is not None

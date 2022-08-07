from datetime import datetime
from enum import Enum
from os import getenv
from typing import Any, Callable

from dotenv import load_dotenv
from praw import Reddit
from praw.models import ListingGenerator, Submission, Subreddit
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

SortType = Enum("SortType", ["HOT", "NEW", "RISING", "TOP", "CONTROVERSIAL"])


def jsonify_submission(submission: Submission) -> dict[str, Any]:
    return {
        "id": submission.id,
        "url": submission.url,
        "title": submission.title,
        "author": submission.author.name if submission.author else None,
        "nsfw": submission.over_18,
        "spoiler": submission.spoiler,
        "selftext": submission.selftext,
        "score": submission.score,
        "created_utc": datetime.utcfromtimestamp(submission.created_utc),
        "shortlink": submission.shortlink,
        "subreddit": submission.subreddit.display_name,
    }


def get_submissions(subreddit: str, load_count: int, sort_type) -> list[Submission]:
    return _get_submissions_with_filtering(subreddit, load_count, sort_type, lambda _: True)


def get_media_submissions(subreddit: str, load_count: int, sort_type) -> list[Submission]:
    return _get_submissions_with_filtering(subreddit, load_count, sort_type, _submission_is_media)


def get_text_submissions(subreddit: str, load_count: int, sort_type) -> list[Submission]:
    return _get_submissions_with_filtering(subreddit, load_count, sort_type, _submission_is_text)


def _get_submissions_with_filtering(
    subreddit: str,
    load_count: int,
    sort_type: SortType,
    submission_filter: Callable[[Submission], bool],
) -> list[Submission]:
    subreddit = _client.subreddit(subreddit)
    submissions_generator = _get_submissions_generator(subreddit, sort_type)
    submissions_generator.limit = load_count
    submissions = _load_submissions(submissions_generator)
    return [submission for submission in submissions if submission_filter(submission)]


def _get_submissions_generator(subreddit: Subreddit, sort_type: SortType) -> ListingGenerator:
    match sort_type:
        case SortType.HOT:
            return subreddit.hot()
        case SortType.NEW:
            return subreddit.new()
        case SortType.RISING:
            return subreddit.rising()
        case SortType.TOP:
            return subreddit.top()
        case SortType.CONTROVERSIAL:
            return subreddit.controversial()
        case _:
            return subreddit.hot()


def _load_submissions(submissions_generator: ListingGenerator) -> list[Submission]:
    try:
        return list(submissions_generator)
    except Redirect:
        return []


def _submission_is_media(submission: Submission) -> bool:
    return submission.url.endswith(_MEDIA_SUBMISSION_URL_SUFFIXES)


def _submission_is_text(submission: Submission) -> bool:
    return submission.selftext_html is not None

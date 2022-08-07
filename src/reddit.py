from datetime import datetime
from enum import Enum
from os import getenv
from typing import Any, Callable

from dotenv import load_dotenv
from praw import Reddit
from praw.models import ListingGenerator, Submission
from praw.models.listing.mixins import BaseListingMixin
from praw.models.listing.mixins.redditor import SubListing
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

SortType = Enum("SortType", ["HOT", "NEW", "TOP", "CONTROVERSIAL"])


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
        "stickied": submission.stickied,
    }


def get_submissions(subreddit: str, limit: int, sort_type) -> list[Submission]:
    return _get_submissions(_client.subreddit(subreddit), limit, sort_type, lambda _: True)


def get_media_submissions(subreddit: str, limit: int, sort_type) -> list[Submission]:
    return _get_submissions(_client.subreddit(subreddit), limit, sort_type, _submission_is_media)


def get_text_submissions(subreddit: str, limit: int, sort_type) -> list[Submission]:
    return _get_submissions(_client.subreddit(subreddit), limit, sort_type, _submission_is_text)


def get_user_submissions(username: str, limit: int, sort_type) -> list[Submission]:
    return _get_submissions(_get_redditor_source(username), limit, sort_type, lambda _: True)


def get_user_media_submissions(username: str, limit: int, sort_type) -> list[Submission]:
    return _get_submissions(_get_redditor_source(username), limit, sort_type, _submission_is_media)


def get_user_text_submissions(username: str, limit: int, sort_type) -> list[Submission]:
    return _get_submissions(_get_redditor_source(username), limit, sort_type, _submission_is_text)


def _get_redditor_source(username: str) -> SubListing:
    return _client.redditor(username).submissions


def _get_submissions(
    source: BaseListingMixin,
    limit: int,
    sort_type: SortType,
    submission_filter: Callable[[Submission], bool],
) -> list[Submission]:
    submissions_generator = _get_submissions_generator(source, sort_type)
    submissions_generator.limit = limit
    submissions = _load_submissions(submissions_generator)
    return [submission for submission in submissions if submission_filter(submission)]


def _get_submissions_generator(source: BaseListingMixin, sort_type: SortType) -> ListingGenerator:
    match sort_type:
        case SortType.HOT:
            return source.hot()
        case SortType.NEW:
            return source.new()
        case SortType.TOP:
            return source.top()
        case SortType.CONTROVERSIAL:
            return source.controversial()
        case _:
            return source.hot()


def _load_submissions(submissions_generator: ListingGenerator) -> list[Submission]:
    try:
        return list(submissions_generator)
    except Redirect:
        return []


def _submission_is_media(submission: Submission) -> bool:
    return submission.url.endswith(_MEDIA_SUBMISSION_URL_SUFFIXES)


def _submission_is_text(submission: Submission) -> bool:
    return submission.selftext_html is not None

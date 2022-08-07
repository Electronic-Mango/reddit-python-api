"""
Module responsible for accessing Reddit API via PRAW.
"""

from datetime import datetime
from typing import Any, Callable

from praw import Reddit
from praw.models import ListingGenerator, Submission
from praw.models.listing.mixins import BaseListingMixin
from praw.models.listing.mixins.redditor import SubListing
from prawcore import Redirect

from settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_CLIENT_USER_AGENT,
    REDDIT_IMAGE_URL_SUFFIXES,
)

_client = Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_CLIENT_USER_AGENT,
)


def jsonify_submission(submission: Submission) -> dict[str, Any]:
    """Change Reddit submission to a JSON-like dict

    Only a selected values are present in resulting JSON:
     - id
     - url
     - title
     - author, or None if author is unavailable
     - nsfw
     - spoiler
     - selftext
     - score
     - created_utc
     - shortlink
     - subreddit
     - stickied

    Args:
        submission (Submission): Reddit submission to JSONify

    Returns:
        dict[str, Any]: dict containing JSONified submission
    """
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


def get_subreddit_submissions(subreddit: str, limit: int, sort_type: str) -> list[Submission]:
    """Get a list of submissions from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort_type (str): "controversial", "top", "new", others are interpreted as "hot"

    Returns:
        list[Submission]: list of all loaded submissions from given subreddit.
    """
    return _get_submissions(_client.subreddit(subreddit), limit, sort_type, lambda _: True)


def get_subreddit_image_submissions(subreddit: str, limit: int, sort_type: str) -> list[Submission]:
    """Get a list of image submissions (images, GIFs) from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given subreddit,
    more submissions will be dropped as part of "image" filtering.
    Submissions are classified as "image" based on their URL suffix.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort_type (str): "controversial", "top", "new", others are interpreted as "hot"

    Returns:
        list[Submission]: list of all loaded image submissions from given subreddit.
    """
    return _get_submissions(_client.subreddit(subreddit), limit, sort_type, _submission_is_image)


def get_subreddit_text_submissions(subreddit: str, limit: int, sort_type: str) -> list[Submission]:
    """Get a list of text submissions from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given subreddit,
    more submissions will be dropped as part of "text" filtering.
    Submissions are classified as "text" if their "selftext" field is not empty.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort_type (str): "controversial", "top", "new", others are interpreted as "hot"

    Returns:
        list[Submission]: list of all loaded text submissions from given subreddit.
    """
    return _get_submissions(_client.subreddit(subreddit), limit, sort_type, _submission_is_text)


def get_user_submissions(username: str, limit: int, sort_type: str) -> list[Submission]:
    """Get a list of submissions from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort_type (str): "controversial", "top", "new", others are interpreted as "hot"

    Returns:
        list[Submission]: list of all loaded submissions from given user.
    """
    return _get_submissions(_get_redditor_source(username), limit, sort_type, lambda _: True)


def get_user_image_submissions(username: str, limit: int, sort_type: str) -> list[Submission]:
    """Get a list of image submissions (images, GIFs) from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given user,
    more submissions will be dropped as part of "image" filtering.
    Submissions are classified as "image" based on their URL suffix.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort_type (str): "controversial", "top", "new", others are interpreted as "hot"

    Returns:
        list[Submission]: list of all loaded image submissions from given user.
    """
    return _get_submissions(_get_redditor_source(username), limit, sort_type, _submission_is_image)


def get_user_text_submissions(username: str, limit: int, sort_type: str) -> list[Submission]:
    """Get a list of text submissions from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given user,
    more submissions will be dropped as part of "text" filtering.
    Submissions are classified as "text" if their "selftext" field is not empty.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort_type (str): "controversial", "top", "new", others are interpreted as "hot"

    Returns:
        list[Submission]: list of all loaded text submissions from given user.
    """
    return _get_submissions(_get_redditor_source(username), limit, sort_type, _submission_is_text)


def _get_redditor_source(username: str) -> SubListing:
    return _client.redditor(username).submissions


def _get_submissions(
    source: BaseListingMixin,
    limit: int,
    sort_type: str,
    submission_filter: Callable[[Submission], bool],
) -> list[Submission]:
    submissions_generator = _get_submissions_generator(source, sort_type)
    submissions_generator.limit = limit
    submissions = _load_submissions(submissions_generator)
    return [submission for submission in submissions if submission_filter(submission)]


def _get_submissions_generator(source: BaseListingMixin, sort_type: str) -> ListingGenerator:
    match sort_type:
        case "new":
            return source.new()
        case "top":
            return source.top()
        case "controversial":
            return source.controversial()
        case _:
            return source.hot()


def _load_submissions(submissions_generator: ListingGenerator) -> list[Submission]:
    try:
        return list(submissions_generator)
    except Redirect:
        return []


def _submission_is_image(submission: Submission) -> bool:
    return submission.url.endswith(REDDIT_IMAGE_URL_SUFFIXES)


def _submission_is_text(submission: Submission) -> bool:
    return submission.selftext is not None

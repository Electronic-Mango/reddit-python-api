"""
Module responsible for accessing Reddit API via PRAW.
"""

from reddit.jsonify import jsonify_submission
from reddit.wrapper import RedditApiWrapper, SortType, Submission

from settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_CLIENT_USER_AGENT,
)

_wrapper = RedditApiWrapper(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_CLIENT_USER_AGENT,
)


def get_subreddit_submissions(subreddit: str, limit: int, sort_type: SortType) -> list[Submission]:
    """Get a list of submissions from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort_type (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded submissions from given subreddit.
    """
    submissions = _wrapper.subreddit_submissions(subreddit, limit, sort_type)
    return list(map(jsonify_submission, submissions))


def get_subreddit_image_submissions(subreddit: str, limit: int, sort_type: SortType) -> list[Submission]:
    """Get a list of image submissions (images, GIFs) from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given subreddit,
    more submissions will be dropped as part of "image" filtering.
    Submissions are classified as "image" based on their URL suffix.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort_type (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded image submissions from given subreddit.
    """
    submissions = _wrapper.subreddit_submissions(subreddit, limit, sort_type)
    submissions = map(jsonify_submission, submissions)
    return list(filter(lambda submission: submission["media_url"], submissions))


def get_subreddit_text_submissions(subreddit: str, limit: int, sort_type: SortType) -> list[Submission]:
    """Get a list of text submissions from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given subreddit,
    more submissions will be dropped as part of "text" filtering.
    Submissions are classified as "text" if their "selftext" field is not empty.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort_type (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded text submissions from given subreddit.
    """
    submissions = _wrapper.subreddit_submissions(subreddit, limit, sort_type)
    submissions = map(jsonify_submission, submissions)
    return list(filter(lambda submission: submission["selftext"], submissions))


def get_user_submissions(username: str, limit: int, sort_type: SortType) -> list[Submission]:
    """Get a list of submissions from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort_type (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded submissions from given user.
    """
    submissions = _wrapper.user_submissions(username, limit, sort_type)
    return list(map(jsonify_submission, submissions))


def get_user_image_submissions(username: str, limit: int, sort_type: SortType) -> list[Submission]:
    """Get a list of image submissions (images, GIFs) from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given user,
    more submissions will be dropped as part of "image" filtering.
    Submissions are classified as "image" based on their URL suffix.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort_type (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded image submissions from given user.
    """
    submissions = _wrapper.user_submissions(username, limit, sort_type)
    submissions = map(jsonify_submission, submissions)
    return list(filter(lambda submission: submission["media_url"], submissions))


def get_user_text_submissions(username: str, limit: int, sort_type: SortType) -> list[Submission]:
    """Get a list of text submissions from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given user,
    more submissions will be dropped as part of "text" filtering.
    Submissions are classified as "text" if their "selftext" field is not empty.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort_type (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded text submissions from given user.
    """
    submissions = _wrapper.user_submissions(username, limit, sort_type)
    submissions = map(jsonify_submission, submissions)
    return list(filter(lambda submission: submission["selftext"], submissions))

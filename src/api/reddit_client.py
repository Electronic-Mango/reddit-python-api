"""
Module responsible for accessing Reddit API via PRAW.
"""

from reddit.parser import parse_submission
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


async def get_subreddit_submissions(subreddit: str, limit: int, sort: SortType) -> list[Submission]:
    """Get a list of submissions from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded submissions from given subreddit.
    """
    submissions = await _wrapper.subreddit_submissions(subreddit, limit, sort)
    return list(map(parse_submission, submissions))


async def get_subreddit_media_submissions(
    subreddit: str, limit: int, sort: SortType
) -> list[Submission]:
    """Get a list of media submissions (images, GIFs, videos) from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given subreddit,
    more submissions will be dropped as part of "media" filtering.
    Submissions are classified as "media" based on present "media_url" key in parsed submission.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded media submissions from given subreddit.
    """
    submissions = await _wrapper.subreddit_submissions(subreddit, limit, sort)
    submissions = map(parse_submission, submissions)
    return list(filter(lambda submission: submission["media_url"], submissions))


async def get_subreddit_text_submissions(
    subreddit: str, limit: int, sort: SortType
) -> list[Submission]:
    """Get a list of text submissions from the given subreddit

    Resulting list can be shorter than "limit" argument if given subreddit has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given subreddit,
    more submissions will be dropped as part of "text" filtering.
    Submissions are classified as "text" if their "selftext" field is not empty.

    Args:
        subreddit (str): name of subreddit to get data from
        limit (int): how many submissions should be loaded
        sort (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded text submissions from given subreddit.
    """
    submissions = await _wrapper.subreddit_submissions(subreddit, limit, sort)
    submissions = map(parse_submission, submissions)
    return list(filter(lambda submission: submission["selftext"], submissions))


async def get_user_submissions(username: str, limit: int, sort: SortType) -> list[Submission]:
    """Get a list of submissions from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded submissions from given user.
    """
    submissions = await _wrapper.user_submissions(username, limit, sort)
    return list(map(parse_submission, submissions))


async def get_user_image_submissions(username: str, limit: int, sort: SortType) -> list[Submission]:
    """Get a list of media submissions (images, GIFs, videos) from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given user,
    more submissions will be dropped as part of "media" filtering.
    Submissions are classified as "media" based on present "media_url" key in parsed submission.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded media submissions from given user.
    """
    submissions = await _wrapper.user_submissions(username, limit, sort)
    submissions = map(parse_submission, submissions)
    return list(filter(lambda submission: submission["media_url"], submissions))


async def get_user_text_submissions(username: str, limit: int, sort: SortType) -> list[Submission]:
    """Get a list of text submissions from the given user

    Resulting list can be shorter than "limit" argument if given user has fewer submissions.
    Additionally "limit" only defines how many submissions are loaded from given user,
    more submissions will be dropped as part of "text" filtering.
    Submissions are classified as "text" if their "selftext" field is not empty.

    Args:
        username (str): name of user to get data from
        limit (int): how many submissions should be loaded
        sort (SortType): sort type to use when accessing submissions

    Returns:
        list[Submission]: list of all loaded text submissions from given user.
    """
    submissions = await _wrapper.user_submissions(username, limit, sort)
    submissions = map(parse_submission, submissions)
    return list(filter(lambda submission: submission["selftext"], submissions))

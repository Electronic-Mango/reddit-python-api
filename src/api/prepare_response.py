"""
Module responsible for preparing responses with Reddit submissions.
"""

from random import choice
from typing import Any, Callable

from flask import abort

from reddit.client import Submission
from reddit.jsonify import jsonify_submission


def prepare_list_response(
    source_name: str,
    load_count: int,
    sort: str,
    submissions_generator: Callable[[str, int, str], list[Submission]],
) -> dict[str, Any]:
    """Prepare JSONified list of Reddit submissions

    Args:
        source_name (str): Name for a given source, like subreddit, or user.
                           Is later used by submissions_generator.
        load_count (int): How many submissions should be loaded.
                          Is later used by submissions_generator.
        sort (str): Sort type, like "hot", "new", "top", "controversial".
                    Is later used by submissions_generator.
        submissions_generator (Callable[[str, int, str], list[Submission]]): Callback generating
                a list of submissions based on previous arguments. source_name is used as first,
                load_count as second and sort as last.

    Returns:
        dict[str, Any]: JSON containing list of generated submissions and their count.
    """
    submissions = _get_submissions_or_abort(source_name, load_count, sort, submissions_generator)
    submissions = [jsonify_submission(submission) for submission in submissions]
    return {"count": len(submissions), "submissions": submissions}


def prepare_random_response(
    source_name: str,
    load_count: int,
    sort: str,
    submissions_generator: Callable[[str, int, str], list[Submission]],
) -> dict[str, Any]:
    """_summary_

    Args:
        source_name (str): Name for a given source, like subreddit, or user.
                           Is later used by submissions_generator.
        load_count (int): How many submissions should be loaded, a random one is picked from them.
                          Is later used by submissions_generator.
                          Is later used by submissions_generator.
        sort (str): Sort type, like "hot", "new", "top", "controversial".
        submissions_generator (Callable[[str, int, str], list[Submission]]): Callback generating
                a list of submissions based on previous arguments. source_name is used as first,
                load_count as second and sort as last.

    Returns:
        dict[str, Any]: JSON containing data of a random generated submission.
    """
    submissions = _get_submissions_or_abort(source_name, load_count, sort, submissions_generator)
    random_submission = choice(submissions)
    return jsonify_submission(random_submission)


def _get_submissions_or_abort(
    source_name: str,
    load_count: int,
    sort: str,
    submissions_generator: Callable[[str, int, str], list[Submission]],
) -> list[Submission]:
    submissions = submissions_generator(source_name, load_count, sort)
    if not submissions:
        abort(404, f"No entries found for {source_name}")
    return submissions
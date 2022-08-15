"""
Module responsible for preparing responses with Reddit submissions.
"""

from random import choice
from typing import Any

from flask import abort

from reddit.client import Submission


def prepare_list_response_or_abort(submissions: list[Submission]) -> dict[str, Any]:
    """Prepare API list response or abort with code 404 if no submissions are present

    Args:
        submissions (list[Submission]): list of Reddit submissions to send back

    Returns:
        dict[str, Any]: JSON containing list of generated submissions and their count
    """
    if not submissions:
        abort(404, "No entries found")
    return {"count": len(submissions), "submissions": submissions}


def prepare_random_response_or_abort(submissions: list[Submission]) -> dict[str, Any]:
    """Prepare API random, single response or abort with code 404 if no submissions are present

    Args:
        submissions (list[Submission]): list of submissions to pick one random from to send back

    Returns:
        dict[str, Any]: JSON containing data of one random submission
    """
    if not submissions:
        abort(404, "No entries found")
    return choice(submissions)

"""
Module responsible for JSONifying Reddit submissions.
"""

from datetime import datetime
from typing import Any

from praw.models import Submission


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

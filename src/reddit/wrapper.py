"""
Wrapper for Reddit API.
Using a wrapper simplifies accessing the API, mostly due to handling OAuth.
"""

from enum import Enum, auto
from time import time_ns
from typing import Any

from requests import Response, get, post
from requests.auth import HTTPBasicAuth

"""Type of all returning submissions"""
Submission = dict[str, Any]

class SortType(Enum):
    """Enum with all viable sorting types"""
    hot = auto()
    top = auto()
    new = auto()
    controversial = auto()


class RedditApiWrapper:
    """Class wrapping Reddit API
    
    Class wrapping calls to Reddit API.
    Handles all necessary URLs, parameters, headers, etc.
    Also handles requesting new OAuth 2.0 access tokens and authorization in general.
    
    Args:
        client_id (str): Reddit app client ID to use for authorization
        client_secret (str): Reddit app client secret to use for authorization
        user_agent (str): user agent used in all Reddit API requests
    """

    _ACCESS_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
    _SUBREDDIT_SUBMISSIONS_URL = "https://oauth.reddit.com/r/{subreddit}/{sort}"
    _USER_SUBMISSIONS_URL = "https://oauth.reddit.com/user/{user}/submitted"
    _AUTH_EXPIRY_OVERHEAD_SECONDS = 60

    def __init__(self, client_id: str, client_secret: str, user_agent: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_agent = user_agent
        self._authorize()

    def _authorize(self) -> None:
        auth_headers = {"User-agent": self._user_agent}
        response = post(
            url=self._ACCESS_TOKEN_URL,
            params={"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(username=self._client_id, password=self._client_secret),
            headers=auth_headers,
        )
        assert response.status_code == 200
        response_content = response.json()
        access_token = response_content["access_token"]
        auth_headers["Authorization"] = f"Bearer {access_token}"
        self._auth_headers = auth_headers
        expires_in = response_content["expires_in"]
        self._access_token_expires_in = time_ns() + expires_in - self._AUTH_EXPIRY_OVERHEAD_SECONDS

    def subreddit_submissions(self, subreddit: str, limit: int, sort: SortType) -> list[Submission]:
        """Get a list of Reddit submissions from the given subreddit

        Args:
            subreddit (str): subreddit to load submissions from
            limit (int): up to how many submissions should be loaded
            sort (SortType): sort type to use when loading submissions

        Returns:
            list[Submission]: list of loaded submissions from the given subreddit
        """
        if self._access_token_expires_in <= time_ns():
            self._authorize()
        url = self._SUBREDDIT_SUBMISSIONS_URL.format(subreddit=subreddit, sort=sort.name)
        response = get(url=url, params={"limit": limit}, headers=self._auth_headers)
        if response.status_code in [401, 403]:
            self._authorize()
            response = get(url=url, params={"limit": limit}, headers=self._auth_headers)
        return self._parse_api_response(response)

    def user_submissions(self, user: str, limit: int, sort: SortType) -> list[Submission]:
        """Get a list of Reddit submissions from the given Reddit user

        Args:
            user (str): Reddit user to load submissions from
            limit (int): up to how many submissions should be loaded
            sort (SortType): sort type to use when loading submissions

        Returns:
            list[Submission]: list of loaded submissions from the Reddit user
        """
        if self._access_token_expires_in <= time_ns():
            self._authorize()
        url = self._USER_SUBMISSIONS_URL.format(user=user, sort=sort.name)
        response = get(url=url, params={"limit": limit, "sort": sort}, headers=self._auth_headers)
        return self._parse_api_response(response)

    def _parse_api_response(self, response: Response) -> list[Submission]:
        assert response.status_code == 200
        return [submission["data"] for submission in response.json()["data"]["children"]]

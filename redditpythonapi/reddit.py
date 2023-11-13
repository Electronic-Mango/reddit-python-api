"""
Wrapper for Reddit API.
Using a wrapper simplifies accessing the API, mostly due to handling OAuth.
"""

from enum import Enum, auto
from logging import getLogger
from time import time_ns
from typing import Any

from httpx import AsyncClient, BasicAuth, Response


class SortType(Enum):
    """Enum with all viable sorting types"""

    HOT = auto()
    TOP = auto()
    NEW = auto()
    CONTROVERSIAL = auto()


class Reddit:
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
    _AUTH_EXPIRY_OVERHEAD_NS = 60_000_000_000

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str = "Reddit Python API (by Electronic-Mango on GitHub)",
    ) -> None:
        self._client_auth = BasicAuth(username=client_id, password=client_secret)
        self._auth_headers = {"User-agent": user_agent}
        self._access_token_expires_in = 0
        self._logger = getLogger(__name__)

    async def subreddit_submissions(
        self, subreddit: str, limit: int, sort: SortType
    ) -> list[dict[str, Any]]:
        """Get a list of Reddit submissions from the given subreddit

        Args:
            subreddit (str): subreddit to load submissions from
            limit (int): up to how many submissions should be loaded
            sort (SortType): sort type to use when loading submissions

        Returns:
            list[Submission]: list of loaded submissions from the given subreddit
        """
        self._logger.info(f"Loading subreddit submissions [{subreddit}] [{limit}] [{sort.name}]")
        url = self._SUBREDDIT_SUBMISSIONS_URL.format(subreddit=subreddit, sort=sort.name.lower())
        params = {"limit": limit}
        return await self._get_submissions(url, params)

    async def user_submissions(self, user: str, limit: int, sort: SortType) -> list[dict[str, Any]]:
        """Get a list of Reddit submissions from the given Reddit user

        Args:
            user (str): Reddit user to load submissions from
            limit (int): up to how many submissions should be loaded
            sort (SortType): sort type to use when loading submissions

        Returns:
            list[Submission]: list of loaded submissions from the Reddit user
        """
        self._logger.info(f"Loading user submissions [{user}] [{limit}] [{sort.name}]")
        url = self._USER_SUBMISSIONS_URL.format(user=user)
        params = {"limit": limit, "sort": sort.name.lower()}
        return await self._get_submissions(url, params)

    async def _authorize(self) -> None:
        self._logger.info("Authorizing")
        response = await self._request_access_token()
        response.raise_for_status()
        response_content = response.json()
        access_token = response_content["access_token"]
        self._auth_headers["Authorization"] = f"Bearer {access_token}"
        expires_in = response_content["expires_in"] * 1_000_000_000
        self._access_token_expires_in = time_ns() + expires_in - self._AUTH_EXPIRY_OVERHEAD_NS

    async def _request_access_token(self) -> Response:
        async with AsyncClient() as client:
            return await client.post(
                url=self._ACCESS_TOKEN_URL,
                params={"grant_type": "client_credentials"},
                auth=self._client_auth,
                headers=self._auth_headers,
            )

    async def _get_submissions(self, url: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        if self._access_token_expires_in <= time_ns():
            self._logger.info("Access token expired, requesting new one")
            await self._authorize()
        response = await self._request_submissions(url, params)
        if response.status_code in [401, 403]:
            self._logger.info(f"Response returned code [{response.status_code}], re-authorizing")
            await self._authorize()
            response = await self._request_submissions(url, params)
        response.raise_for_status()
        return [submission["data"] for submission in response.json()["data"]["children"]]

    async def _request_submissions(self, url: str, params: dict[str, Any]) -> Response:
        async with AsyncClient() as client:
            return await client.get(url=url, params=params, headers=self._auth_headers)

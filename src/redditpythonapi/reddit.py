"""
Wrapper for Reddit API.
Using a wrapper simplifies accessing the API, mostly due to handling OAuth.
"""

from enum import StrEnum
from logging import getLogger
from time import time_ns
from typing import Any

from httpx import AsyncClient, BasicAuth, Response

Article = dict[str, Any]


class ArticlesSortType(StrEnum):
    """Enum with all viable sorting types"""

    HOT = "hot"
    NEW = "new"
    RISING = "rising"
    TOP = "top"
    CONTROVERSIAL = "controversial"


class ArticlesSortTime(StrEnum):
    """Enum with all viable sort times"""

    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    ALL = "all"


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
    _SUBREDDIT_ARTICLES_URL = "https://oauth.reddit.com/r/{subreddit}/{sort}"
    _USER_ARTICLES_URL = "https://oauth.reddit.com/user/{user}/submitted"
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

    async def subreddit_articles(
        self,
        subreddit: str,
        sort: ArticlesSortType | None = None,
        time: ArticlesSortTime | None = None,
        limit: int | None = None,
    ) -> list[Article]:
        """Get a list of Reddit articles from the given subreddit

        Args:
            subreddit (str): subreddit to load articles from
            sort (ArticlesSortType | None): sort type to use when loading articles, "hot" by default
            time (ArticlesSortTime | None): sort time to use when loading articles,
                                            by default not passed onto Reddit API
            limit (int | None): up to how many articles should be loaded,
                                by default not passed onto Reddit API

        Returns:
            list[Article]: list of loaded articles from the given subreddit
        """
        self._logger.info(f"Loading subreddit articles [{subreddit}] [{sort}] [{time}] [{limit}]")
        sort = sort or ArticlesSortType.HOT
        url = self._SUBREDDIT_ARTICLES_URL.format(subreddit=subreddit, sort=sort.value)
        params = self._prepare_params(limit=limit, time=time)
        return await self._get_articles(url, params)

    async def user_articles(
        self,
        user: str,
        sort: ArticlesSortType | None = None,
        time: ArticlesSortTime | None = None,
        limit: int | None = None,
    ) -> list[Article]:
        """Get a list of Reddit articles from the given Reddit user

        Args:
            user (str): Reddit user to load articles from
            sort (ArticlesSortType | None): sort type to use when loading articles,
                                            by default not passed onto Reddit API
            time (ArticlesSortTime | None): sort time to use when loading articles,
                                            by default not passed onto Reddit API
            limit (int | None): up to how many articles should be loaded,
                                by default not passed onto Reddit API

        Returns:
            list[Article]: list of loaded articles from the Reddit user
        """
        self._logger.info(f"Loading user articles [{user}] [{sort}] [{time}] [{limit}]")
        url = self._USER_ARTICLES_URL.format(user=user)
        params = self._prepare_params(limit=limit, sort=sort, time=time)
        return await self._get_articles(url, params)

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

    def _prepare_params(
        self,
        sort: ArticlesSortType | None = None,
        time: ArticlesSortTime | None = None,
        limit: int | None = None,
    ):
        return {
            **({"sort": sort.value} if sort is not None else {}),
            **({"t": time.value} if time is not None else {}),
            **({"limit": limit} if limit is not None else {}),
        }

    async def _get_articles(self, url: str, params: dict[str, Any]) -> list[Article]:
        if self._access_token_expires_in <= time_ns():
            self._logger.info("Access token expired, requesting new one")
            await self._authorize()
        response = await self._request_articles(url, params)
        if response.status_code in [401, 403]:
            self._logger.info(f"Response returned code [{response.status_code}], re-authorizing")
            await self._authorize()
            response = await self._request_articles(url, params)
        response.raise_for_status()
        return [article["data"] for article in response.json()["data"]["children"]]

    async def _request_articles(self, url: str, params: dict[str, Any]) -> Response:
        async with AsyncClient() as client:
            return await client.get(url=url, params=params, headers=self._auth_headers)

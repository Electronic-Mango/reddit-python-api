from enum import Enum, auto
from time import time_ns
from typing import Any

from requests import Response, get, post
from requests.auth import HTTPBasicAuth

Submission = dict[str, Any]


class SortType(Enum):
    hot = auto()
    top = auto()
    new = auto()
    controversial = auto()


class RedditApiWrapper:
    ACCESS_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
    SUBREDDIT_SUBMISSIONS_URL = "https://oauth.reddit.com/r/{subreddit}/{sort}"
    USER_SUBMISSIONS_URL = "https://oauth.reddit.com/user/{user}/submitted"
    AUTH_EXPIRY_OVERHEAD_SECONDS = 60

    def __init__(self, client_id: str, client_secret: str, user_agent: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_agent = user_agent
        self.authorize()

    def authorize(self) -> None:
        auth_headers = {"User-agent": self._user_agent}
        response = post(
            url=self.ACCESS_TOKEN_URL,
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
        self._access_token_expires_in = time_ns() + expires_in - self.AUTH_EXPIRY_OVERHEAD_SECONDS

    def subreddit_submissions(self, subreddit: str, count: int, sort: SortType) -> list[Submission]:
        if self._access_token_expires_in <= time_ns():
            self.authorize()
        url = self.SUBREDDIT_SUBMISSIONS_URL.format(subreddit=subreddit, sort=sort.name)
        response = get(url=url, params={"limit": count}, headers=self._auth_headers)
        if response.status_code in [401, 403]:
            self.authorize()
            response = get(url=url, params={"limit": count}, headers=self._auth_headers)
        return self.parse_api_response(response)

    def user_submissions(self, user: str, count: int, sort: SortType) -> list[Submission]:
        if self._access_token_expires_in <= time_ns():
            self.authorize()
        url = self.USER_SUBMISSIONS_URL.format(user=user, sort=sort.name)
        response = get(url=url, params={"limit": count, "sort": sort}, headers=self._auth_headers)
        return self.parse_api_response(response)

    def parse_api_response(self, response: Response) -> list[Submission]:
        assert response.status_code == 200
        return [submission["data"] for submission in response.json()["data"]["children"]]

"""
Module storing all configuration data used by the API, read from a settings YAML file.
Default settings YAML - "settings.yml" - is loaded from the execution environment root.

All information can be either read from the default "settings.yml" file, or from overriding custom
one from path under "CUSTOM_SETTINGS_PATH" environment variable.
This custom one doesn't need to specify all parameters, just the new ones.
"""

from functools import reduce
from os import getenv
from typing import Any

from dotenv import load_dotenv
from mergedeep import merge
from yaml import safe_load

load_dotenv()
_DEFAULT_SETTINGS_PATH = "settings.yml"
_CUSTOM_SETTINGS_PATH_VARIABLE_NAME = "CUSTOM_SETTINGS_PATH"
_CUSTOM_SETTINGS_PATH = getenv(_CUSTOM_SETTINGS_PATH_VARIABLE_NAME)


def _load_settings(settings_path: str) -> dict[str, Any]:
    with open(settings_path) as settings_yaml:
        return safe_load(settings_yaml)


_SETTINGS = merge(
    _load_settings(_DEFAULT_SETTINGS_PATH),
    _load_settings(_CUSTOM_SETTINGS_PATH) if _CUSTOM_SETTINGS_PATH else {},
)


def _load_config(*keys: tuple[str]) -> Any:
    return reduce(lambda table, key: table[key], keys, _SETTINGS)


API_HOST = _load_config("api", "host")
API_PORT = _load_config("api", "port")
API_AUTHORIZATION_HEADER_NAME = _load_config("api", "authorization_header", "name")
API_AUTHORIZATION_HEADER_VALUE = _load_config("api", "authorization_header", "expected_value")
DEFAULT_LOAD_COUNT = int(_load_config("api", "reddit", "default_load_count"))
DEFAULT_SUBREDDIT = _load_config("api", "reddit", "default_subreddit")

REDDIT_CLIENT_ID = _load_config("reddit", "client", "id")
REDDIT_CLIENT_SECRET = _load_config("reddit", "client", "secret")
REDDIT_CLIENT_USER_AGENT = _load_config("reddit", "client", "user_agent")

"""
Module storing all configuration data used by the API.

All information can be either read from a "settings.yml" file, or from environment variables,
where environment variables will be used with higher priority.

"settings.yml" is loaded either from the execution environment root,
or from a path given by "SETTINGS_YAML_PATH" environment variable.

In order to overwrite values from YAML the varialbe must follow a specific naming convention
of all nested keys separated by an "_", like "api_host", "api_reddit_default_load_count", etc.
"""

from os import getenv

from dotenv import load_dotenv
from yaml import safe_load

load_dotenv()

_DEFAULT_SETTINGS_YAML_PATH = "settings.yml"
_SETTINGS_YAML_PATH = getenv("SETTINGS_YAML_PATH", _DEFAULT_SETTINGS_YAML_PATH)
with open(_SETTINGS_YAML_PATH) as settings_yaml:
    _SETTINGS_YAML = safe_load(settings_yaml)


def _load_config_from_yaml(*keys: tuple[str]) -> str:
    value = _SETTINGS_YAML
    for key in keys:
        value = value[key]
    return value


def _load_config(*keys: tuple[str]) -> str:
    env_name = "_".join(keys)
    env_value = getenv(env_name)
    return env_value if env_value else _load_config_from_yaml(*keys)


API_HOST = _load_config("api", "host")
API_PORT = _load_config("api", "port")
DEFAULT_LOAD_COUNT = int(_load_config("api", "reddit", "default_load_count"))
DEFAULT_SUBREDDIT = _load_config("api", "reddit", "default_subreddit")
REDDIT_CLIENT_ID = _load_config("reddit", "client", "id")
REDDIT_CLIENT_SECRET = _load_config("reddit", "client", "secret")
REDDIT_CLIENT_USER_AGENT = _load_config("reddit", "client", "user_agent")
REDDIT_MEDIA_URL_SUFFIXES = tuple(_load_config("reddit", "media_url_suffixes"))

# Reddit API

[![CodeQL](https://github.com/Electronic-Mango/reddit-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/reddit-api/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/reddit-api/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api/actions/workflows/flake8.yml)

A simple Reddit API allowing accessing both subreddit and user submissions, build with [`PRAW`](https://github.com/praw-dev/praw) and [`Flask`](https://github.com/pallets/flask/).



## Requirements

This API was built using `Python 3.10` and it requires at least version `3.10` due to used `match-case` statement.

Full list of Python requirements is in `requirements.txt` file.


## Configuration

### API parameters

API configuration can be done through a YAML configuration file.
By default `settings.yml` from the project root is used, however you can override path to this file via `SETTINGS_YAML_PATH` environment variable.
In default `settings.yml` parameters are filled with some sensible defaults.
You can check the file itself for their detailed description.

Every field from `settings.yml` can be overwritten via environment variables.
Their names have to match all keys leading to specific value separated by `_`.
For example, values for `reddit` - `client` - `id` and `secret` can be configured via `reddit_client_id` and `reddit_client_secret` environment variables, without modifying used `settings.yml`.

Variables can also be loaded from `.env` file from the project root.
You can put all your custom configuration, like Reddit app configuration, into `.env` and keep it without modifying project files.

### Reddit app & required parameters

To run the API you need to first register a Reddit app at https://old.reddit.com/prefs/apps/.
There are two fields which need to be filled in `reddit` - `client` section in `settings.yml` based on your app - `id` and `secret`.
No other data is necessary, since the API works in `read-only` mode.

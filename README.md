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


### Docker

There's a `Dockerfile` in the repo, which will build a Docker image for the API using `python:3.10-slim` as base.
You can set all configuration parameters using environment variables for Docker container, rather than modifying project files before building.

You can also use `docker-compose.yml` to build and start the container via:
```
docker compose up -d --build
```
Compose will use `.env` file in project root for any additional configuration, like [Reddit app ID and secret](#reddit-app-&-required-parameters).

By default Docker Compose will set port where API is listening for requests to `80`.
This port is also mapped to local port `3001`.
You can use it to access to API running in a container.



## Running the API

First you need to register a Reddit app and note its ID and secret.


###  From source

 1. Install all packages from `requirements.txt`
 1. Fill Reddit app ID and secret either in `settings.yml` in `.env` or as environment variables
 1. Run `src/main.py` via Python


### Docker

 1. Fill Reddit app ID and secret in `.env` in project root
 1. Run `docker compose up -d --build`

You can skip `--build` flag on subsequent runs if you didn't change the source code.

`.env` is not added to the Docker image, just used as a source for environment variables.
So if you make any changes there, just restart the container.
There's no need to rebuild the image.



## Filtering and submission types

Other than all submissions, API allows for filtering submission types.
The two filters are:

 - `text` - all submissions where `selftext` is not empty
 - `image` - all submissions where URL ends with values from `settings.yml`, by default `.jpg`, `.jpeg`, `.png` and `.gif`



## Load count

When specifying how many submissions should be loaded the final count can be lower.

For all submissions this can occur if a given subreddit or user has less submissions than specified.

For text and image submissions the passed value only determines how many submissions are loaded from Reddit overall.
This value can be later lowered as only specific type of submissions are filtered from the list of all submissions.
Not additional submission are loaded after filtering.

Load count also impacts retrieving one random submission.
This one random submission is picked from a loaded selection, instead of sending all of them.
Actual count of submissions to pick from can be lowered due to additional filtering, as before.

Still, the higher the load count the lower the odds of selecting the same random submission on subsequent API calls.

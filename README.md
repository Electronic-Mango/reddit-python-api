# Reddit API API

[![CodeQL](https://github.com/Electronic-Mango/reddit-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/reddit-api/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/reddit-api/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api/actions/workflows/flake8.yml)

A simple Reddit REST API allowing accessing both subreddit and user submissions, build with [`Flask`](https://github.com/pallets/flask/).



## Table of contents

 - [Introduction and requirements](#introduction-and-requirements)
 - [Configuration](#configuration)
   - [API parameters](#api-parameters)
   - [Reddit app & required parameters](#reddit-app---required-parameters)
   - [Docker](#docker)
 - [Authorization](#authorization)
 - [Running the API](#running-the-api)
   - [From source](#from-source)
   - [Docker](#docker-1)
 - [API endpoints](#api-endpoints)
   - [Get a list of submissions from a subreddit](#get-a-list-of-submissions-from-a-subreddit)
   - [Get one random submission from a subreddit](#get-one-random-submission-from-a-subreddit)
   - [Get a list of submissions from a Reddit user](#get-a-list-of-submissions-from-a-reddit-user)
   - [Get a random submission from a Reddit user](#get-a-random-submission-from-a-reddit-user)
 - [Filtering and submission types](#filtering-and-submission-types)
 - [Load count](#load-count)



## Introduction and requirements

This REST API was built using [`Flask`](https://github.com/pallets/flask/) and `Python 3.10`.
Python version at least `3.10` is required.

Full list of Python requirements is in `requirements.txt` file.

Technically this API only *wraps* parts of official Reddit API, thus *Reddit API **API***.
However, accessing Reddit API itself through external services is quite cumbersome, due to necessary OAuth 2.0 authorization.
This API allows external services to access API through simple HTTP requests, without worrying about access tokens, Reddit app client, etc.
It also allows for simple access to specific services, like reading only one random submission or reading only media or text submissions, without any additional processing.

No additional API wrapper was used, this API accesses Reddit API directly.

No data is stored by the API.
Reddit is accessed in `read-only` mode.
API requests can optionally be authenticated based on request header.



## Configuration

### API parameters

API configuration can be done through a YAML configuration file.
By default `settings.yml` from the project root is used, which has some sensible defaults, other than [Reddit API client ID and secret](#reddit-app-&-required-parameters).

You can overwrite values from default `settings.yml` by providing a custom one under path from `CUSTOM_SETTINGS_PATH` environment variable.
In this custom YAML you can provide only parameters which you want to overwrite.
If parameter is absent in the custom one, then default value from `settings.yml` will be used.

Value for `CUSTOM_SETTINGS_PATH` can also be provided via `.env` file in the project root.


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

Compose allows using `custom_settings.yml` in project root for custom configuration, like [Reddit app ID and secret](#reddit-app-&-required-parameters) without modifying project files.
By default this file will be loaded into the image, along with all `.yml` files from the project root.

You can get around this by modifying value of `CUSTOM_SETTINGS_PATH` in `docker-compose.yml` to point to a file in a mounted volume.

Default port where API requests are handled is `8080`, which is mapped to local port `3001`.



## Authorization

Api has a basic authorization mechanism based on request header.
You can set authorization header name and expected value in `settings.yml` in `api` - `authorization_header` - `name` and `expected_value`.

If either of them is empty authorization will be disabled and all requests will be accepted.

If both fields are filled, then any request which doesn't have a header named `name` with value `expected_value` will be rejected with code `401`.

By default, without any changes to `settings.yml` authorization is disabled.



## Running the API

First you need to register a Reddit app and note its ID and secret.


###  From source

 1. Install all packages from `requirements.txt`
 1. Fill Reddit app ID and secret either in `settings.yml` or in a custom one
 1. Run `src/main.py` via Python


### Docker

 1. Fill Reddit app ID and secret in `settings.yml` or in `custom_settings.yml`
 1. Run `docker compose up -d --build`

You can skip `--build` flag on subsequent runs if you didn't change the source code, but keep in mind that by default `custom_settings.yml` is added to the docker image.
Any changes there will require image rebuild.

You can get around this by modifying value of `CUSTOM_SETTINGS_PATH` in `docker-compose.yml` to point to a file in a mounted volume.



## API endpoints

All endpoints are accessible via `GET` requests.
If request authorization is configured incoming requests needs to have correct header and its value.

### Get a list of submissions from a subreddit

Endpoint:
```
/subreddit/{submission_type}/{subreddit_name}/{load_count}/{sort_type}
```

|Parameter|Description|Optional|Default value|
|-|-|-|-|
|`{submission_type}`|Whether to load all submissions, only text or only images|No||
|`{subreddit_name}`|Name of subreddit to load submissions from, including `all` and `popular`|Yes|`all`|
|`{load_count}`|How many submissions to load|Yes|`50`|
|`{sort_type}`|Which Reddit sorting type to use when loading submissions|Yes|`hot`|

`{submission_type}` can be one of the following:

 - `submission` - all submissions
 - `media` - only media submissions
 - `text` - only submissions where `selftext` is not empty

`{sort_type}` can be one of the following:

 - `top`
 - `new`
 - `controversial`
 - `hot`

`{load_count}` and `{sort_type}` can be ommited, but both have to be specified when you want to specify `{sort_type}`.


Example request:
```
GET /subreddit/submission/wholesomememes/3/top
```

Example response:
```json
{
  "count": 3,
  "submissions": [
    {
      "author": "VictorJ45",
      "created_utc": "Mon, 23 Sep 2019 19:51:51 GMT",
      "id": "d8bvvm",
      "nsfw": false,
      "score": 206153,
      "selftext": "",
      "shortlink": "https://redd.it/d8bvvm",
      "spoiler": false,
      "stickied": false,
      "subreddit": "wholesomememes",
      "title": "What a considerate man",
      "url": "https://i.redd.it/eihhjg3veeo31.jpg"
    },
    {
      "author": "TisAubrey",
      "created_utc": "Sat, 14 Mar 2020 11:51:52 GMT",
      "id": "fih6k8",
      "nsfw": false,
      "score": 183474,
      "selftext": "",
      "shortlink": "https://redd.it/fih6k8",
      "spoiler": false,
      "stickied": false,
      "subreddit": "wholesomememes",
      "title": "Wholesome meeting from Tumblr",
      "url": "https://i.redd.it/l9kr8x9xmmm41.jpg"
    },
    {
      "author": "GolfDadNotes",
      "created_utc": "Fri, 20 Nov 2020 04:05:54 GMT",
      "id": "jxi6p6",
      "nsfw": false,
      "score": 180824,
      "selftext": "",
      "shortlink": "https://redd.it/jxi6p6",
      "spoiler": false,
      "stickied": false,
      "subreddit": "wholesomememes",
      "title": "As real as it gets : )",
      "url": "https://i.redd.it/jr4p03glkb061.jpg"
    }
  ]
}
```


### Get one random submission from a subreddit

Endpoint:
```
/subreddit/{submission_type}/random/{subreddit_name}/{load_count}/{sort_type}
```

All parameters are the same as for [loading a list of submissions for a subreddit](#get-a-list-of-submissions-from-a-subreddit).

`{load_count}` determines how many submissions will be loaded, a random one will be selected from them.


Example request:
```
GET /subreddit/text/random/all/100/top
```

Example response:
```json
{
  "author": "Yorkshire45",
  "created_utc": "Sat, 09 Feb 2019 01:43:40 GMT",
  "id": "aonp75",
  "nsfw": false,
  "score": 219186,
  "selftext": "Damn... this got big...",
  "shortlink": "https://redd.it/aonp75",
  "spoiler": false,
  "stickied": false,
  "subreddit": "Showerthoughts",
  "title": "Whoever created the tradition of not seeing the bride in the wedding dress beforehand saved countless husbands everywhere from hours of dress shopping and will forever be a hero to all men.",
  "url": "https://www.reddit.com/r/Showerthoughts/comments/aonp75/whoever_created_the_tradition_of_not_seeing_the/"
}
```


### Get a list of submissions from a Reddit user

Endpoint:
```
/user/{submission_type}/{user_name}/{load_count}/{sort_type}
```

All parameters are the same as for [loading a list of submissions for a subreddit](#get-a-list-of-submissions-from-a-subreddit), except for providing a Reddit username instead of subreddit name.
Username parameter is required, unlike subreddit.

Example request:
```
GET /user/media/cme_t/3
```

Example response:
```json
{
  "count": 2,
  "submissions": [
    {
      "author": "CME_T",
      "created_utc": "Mon, 25 Jul 2022 16:08:12 GMT",
      "id": "w7stzz",
      "nsfw": false,
      "score": 5284,
      "selftext": "",
      "shortlink": "https://redd.it/w7stzz",
      "spoiler": false,
      "stickied": false,
      "subreddit": "TheWeeklyRoll",
      "title": "Ch. 124. \"Common knowledge\"",
      "url": "https://i.redd.it/fzworhhimqd91.jpg"
    },
    {
      "author": "CME_T",
      "created_utc": "Mon, 25 Jul 2022 16:08:00 GMT",
      "id": "w7stti",
      "nsfw": false,
      "score": 1901,
      "selftext": "",
      "shortlink": "https://redd.it/w7stti",
      "spoiler": false,
      "stickied": false,
      "subreddit": "DnD",
      "title": "[Art][OC] The Weekly Roll Ch. 124. \"Common knowledge\"",
      "url": "https://i.redd.it/4kid37rjmqd91.jpg"
    }
  ]
}
```

Notice that 3 media submissions were requested, but response only contains 2.
It's because out of 3 loaded submissions only 2 were images.

Also, since `{sort_type}` was omitted default value of `hot` was used.


### Get a random submission from a Reddit user

Endpoint:
```
/user/{submission_type}/random/{user_name}/{load_count}/{sort_type}
```

All parameters are the same as for [loading a list of submissions for a Reddit user](#get-a-list-of-submissions-from-a-reddit-user).

Example request:
```
GET /user/media/random/cme_t/
```

Example response:
```json
{
  "author": "CME_T",
  "created_utc": "Mon, 25 Jul 2022 16:08:00 GMT",
  "id": "w7stti",
  "nsfw": false,
  "score": 1900,
  "selftext": "",
  "shortlink": "https://redd.it/w7stti",
  "spoiler": false,
  "stickied": false,
  "subreddit": "DnD",
  "title": "[Art][OC] The Weekly Roll Ch. 124. \"Common knowledge\"",
  "url": "https://i.redd.it/4kid37rjmqd91.jpg"
}
```

Since both `{load_count}` and `{sort_type}` were omitted, the default values of `50` and `hot` were used.


## Filtering and submission types

Other than all submissions, API allows for filtering submission types.
The two filters are `text` and `media`.

For `text` all submissions where `selftext` is not empty are selected.

For `media` there are two cases, one for images and one for videos:

 - images are detected based on `i.redd.it` domain **OR** `post_hint` equal to `image`, since not all subreddits have `post_hint`
 - videos are detected based on `v.redd.it` domain **AND** `is_video` equal to `True`, there are some posts where domain is `v.redd.it`, but there're no necessary URLs

In case of videos, resulting `media_url` URL has `?source=fallback` trimmed out, so it ends with file extension.



## Load count

When specifying how many submissions should be loaded the final count can be lower.

For all submissions this can occur if a given subreddit or user has less submissions than specified.

For text and media submissions the passed value only determines how many submissions are loaded from Reddit overall.
This value can be later lowered as only specific type of submissions are filtered from the list of all submissions.
Not additional submissions are loaded after filtering.

Load count also impacts retrieving one random submission.
This one random submission is picked from a loaded selection, instead of sending all of them.
Actual count of submissions to pick from can be lowered due to additional filtering, as before.

Still, the higher the load count the lower the odds of selecting the same random submission on subsequent API calls.

# Reddit Python API

[![CodeQL](https://github.com/Electronic-Mango/reddit-python-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api-api/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/reddit-python-api/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api-api/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/reddit-python-api/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/reddit-api-api/actions/workflows/flake8.yml)
[![PyPI version](https://badge.fury.io/py/reddit-python-api.svg)](https://badge.fury.io/py/reddit-python-api)

A simple read-only Reddit Python API allowing access to both subreddit and user articles, build with [`httpx`](https://www.python-httpx.org/).



## Table of contents

  * [Table of contents](#table-of-contents)
  * [Introduction and requirements](#introduction-and-requirements)
  * [Installation](#installation)
  * [Reddit app & configuration](#reddit-app--configuration)
  * [Usage](#usage)
    * [Create the API](#create-the-api)
    * [Get a list of articles in a subreddit](#get-a-list-of-articles-in-a-subreddit)
    * [Get a list of user articles](#get-a-list-of-user-articles)
    * [Sort types](#sort-types)
    * [Returned articles type](#returned-articles-type)



## Introduction and requirements

This Python API was built using [`httpx`](https://www.python-httpx.org/) and `Python 3.10`.
Python version at least `3.10` is required.

Full list of Python requirements is in `requirements.txt` file.

No additional API wrapper was used (like [PRAW](https://github.com/praw-dev/praw)), Reddit API is accessed directly.
It should be much faster when accessing a list of articles.

No data is stored.
**Reddit is accessed in `read-only` mode.**


Currently, this API allows access to articles in either subreddits or from users.
It doesn't access comments.



## Installation

Project is available in [PyPi](https://pypi.org/project/reddit-python-api/):
```bash
pip install reddit-python-api
```



## Reddit app & configuration

In order to use this API you need to create a Reddit app at https://old.reddit.com/prefs/apps/.
Two parameters are required `client id` and `secret` from your app.
Those values will be used to acquire OAuth 2.0 token from Reddit API itself. 

No other data is necessary, since the API works in `read-only` mode.

When creating the API you can also specify user agent used for communication with Reddit API.
By default `Reddit Python API (by Electronic-Mango on GitHub)` is used.
Reddit required a meaningful user agent to be provided by apps.



## Usage

### Create the API

Two parameters are required - app id and secret:
```python
from redditpythonapi import Reddit

reddit = Reddit("your client ID", "your app secret") 
```

You can also specify user-agent:
```python
from redditpythonapi import Reddit

reddit = Reddit("your client ID", "your app secret", "custom user agent") 
```


### Get a list of articles in a subreddit

```python
reddit = Reddit("your client ID", "your app secret")
# reddit.subreddit_articles("subreddit name", load_count, sort_type)
articles = reddit.subreddit_articles("Python", 10, ArticlesSortType.HOT)
```
First argument is a name of a subreddit.

Second argument specifies how many articles should be loaded.
API can return lower number if there are fewer articles in a given subreddit than provided.

Third argument specifies sort type.
Following sort types are supported:
```python
ArticlesSortType.HOT
ArticlesSortType.NEW
ArticlesSortType.RISING
ArticlesSortType.TOP
ArticlesSortType.CONTROVERSIAL
```


### Get a list of user articles

```python
reddit = Reddit("your client ID", "your app secret")
# reddit.user_articles("username", load_count, sort_type)
articles = reddit.user_articles("spez", 20, ArticlesSortType.CONTROVERSIAL)
```
General usage is the same as for subreddits.


### Sort types

Sort types are available in `ArticlesSortType` enum. These sort types are available:
```python
ArticlesSortType.HOT
ArticlesSortType.NEW
ArticlesSortType.RISING
ArticlesSortType.TOP
ArticlesSortType.CONTROVERSIAL
```


### Returned articles type

Returned type is a list of articles, where each article is a `Submission`.
`Submission` is just an alias to `dict[str, Any]`.
Returned data is directly representing JSON returned by official Reddit API, there are no modification to responses.

You can check official Reddit API documentation for:
 * users - https://www.reddit.com/dev/api/#GET_user_{username}_submitted
 * subreddits - https://www.reddit.com/dev/api/#GET_hot (and other endpoints for different sort types)

Returned dicts are [`listings`](https://www.reddit.com/dev/api/#listings) directly from official Reddit API.
Article contents are quite long, but I've left their additional parsing the user.
Here is an example of one article dict:
```python
{
    'approved_at_utc': None,
    'subreddit': 'wow',
    'selftext': 'https://youtu.be/IHZru-6M8BY\n\nJason Hall, currently an indie developer and former Blizzard employee said in one of his videos\n\n&gt;A $15 microtransaction horse made more money than StarCraft 2\n\nHe worked two years of overtime on StarCraft 2: Wings of Liberty. And the entire game ended up making less money for Blizzard than a single mount in World of Warcraft.',
    'author_fullname': 't2_gnuby',
    'saved': False,
    'mod_reason_title': None,
    'gilded': 0,
    'clicked': False,
    'title': '$15 horse for WoW made more money than StarCraft 2: Wings of Liberty',
    'link_flair_richtext': [
        {
            'e': 'text',
            't': 'Discussion'
        }
    ],
    'subreddit_name_prefixed': 'r/wow',
    'hidden': False,
    'pwls': 6,
    'link_flair_css_class': 'discussion',
    'downs': 0,
    'thumbnail_height': None,
    'top_awarded_type': None,
    'hide_score': False,
    'name': 't3_17tpwfa',
    'quarantine': False,
    'link_flair_text_color': 'dark',
    'upvote_ratio': 0.94,
    'author_flair_background_color': None,
    'subreddit_type': 'public',
    'ups': 2303,
    'total_awards_received': 0,
    'media_embed': {
        
    },
    'thumbnail_width': None,
    'author_flair_template_id': None,
    'is_original_content': False,
    'user_reports': [
        
    ],
    'secure_media': None,
    'is_reddit_media_domain': False,
    'is_meta': False,
    'category': None,
    'secure_media_embed': {
        
    },
    'link_flair_text': 'Discussion',
    'can_mod_post': False,
    'score': 2303,
    'approved_by': None,
    'is_created_from_ads_ui': False,
    'author_premium': False,
    'thumbnail': 'self',
    'edited': False,
    'author_flair_css_class': None,
    'author_flair_richtext': [
        
    ],
    'gildings': {
        
    },
    'post_hint': 'self',
    'content_categories': None,
    'is_self': True,
    'mod_note': None,
    'created': 1699812579.0,
    'link_flair_type': 'richtext',
    'wls': 6,
    'removed_by_category': None,
    'banned_by': None,
    'author_flair_type': 'text',
    'domain': 'self.wow',
    'allow_live_comments': True,
    'selftext_html': '&lt;!-- SC_OFF --&gt;&lt;div class="md"&gt;&lt;p&gt;&lt;a href="https://youtu.be/IHZru-6M8BY"&gt;https://youtu.be/IHZru-6M8BY&lt;/a&gt;&lt;/p&gt;\n\n&lt;p&gt;Jason Hall, currently an indie developer and former Blizzard employee said in one of his videos&lt;/p&gt;\n\n&lt;blockquote&gt;\n&lt;p&gt;A $15 microtransaction horse made more money than StarCraft 2&lt;/p&gt;\n&lt;/blockquote&gt;\n\n&lt;p&gt;He worked two years of overtime on StarCraft 2: Wings of Liberty. And the entire game ended up making less money for Blizzard than a single mount in World of Warcraft.&lt;/p&gt;\n&lt;/div&gt;&lt;!-- SC_ON --&gt;',
    'likes': None,
    'suggested_sort': None,
    'banned_at_utc': None,
    'view_count': None,
    'archived': False,
    'no_follow': False,
    'is_crosspostable': False,
    'pinned': False,
    'over_18': False,
    'preview': {
        'images': [
            {
                'source': {
                    'url': 'https://external-preview.redd.it/aTydt70E_WWF4CDra361TKJGXyuZfwQ_WUkymcp6gW8.jpg?auto=webp&amp;s=22796fd51cff670774bfdc6c30fcc5681afaaab6',
                    'width': 480,
                    'height': 360
                },
                'resolutions': [
                    {
                        'url': 'https://external-preview.redd.it/aTydt70E_WWF4CDra361TKJGXyuZfwQ_WUkymcp6gW8.jpg?width=108&amp;crop=smart&amp;auto=webp&amp;s=6038c06ccc24cd82791506a765b92a96c4481a7d',
                        'width': 108,
                        'height': 81
                    },
                    {
                        'url': 'https://external-preview.redd.it/aTydt70E_WWF4CDra361TKJGXyuZfwQ_WUkymcp6gW8.jpg?width=216&amp;crop=smart&amp;auto=webp&amp;s=1b6308d7254313e680e6f8a995fe2ebe11c667a7',
                        'width': 216,
                        'height': 162
                    },
                    {
                        'url': 'https://external-preview.redd.it/aTydt70E_WWF4CDra361TKJGXyuZfwQ_WUkymcp6gW8.jpg?width=320&amp;crop=smart&amp;auto=webp&amp;s=afb31085dde1286d636a2bdff992cdfccf744653',
                        'width': 320,
                        'height': 240
                    }
                ],
                'variants': {
                    
                },
                'id': 'aqHslU2jfEu8nGDHD1GfMh4aADRzrHE6jlApmtUPZYU'
            }
        ],
        'enabled': False
    },
    'all_awardings': [
        
    ],
    'awarders': [
        
    ],
    'media_only': False,
    'link_flair_template_id': 'ad4fefe2-494b-11ea-9fda-0ecf49ab1e6d',
    'can_gild': False,
    'spoiler': False,
    'locked': False,
    'author_flair_text': None,
    'treatment_tags': [
        
    ],
    'visited': False,
    'removed_by': None,
    'num_reports': None,
    'distinguished': None,
    'subreddit_id': 't5_2qio8',
    'author_is_blocked': False,
    'mod_reason_by': None,
    'removal_reason': None,
    'link_flair_background_color': '',
    'id': '17tpwfa',
    'is_robot_indexable': True,
    'report_reasons': None,
    'author': 'ErgoNonSim',
    'discussion_type': None,
    'num_comments': 563,
    'send_replies': False,
    'whitelist_status': 'all_ads',
    'contest_mode': False,
    'mod_reports': [
        
    ],
    'author_patreon_flair': False,
    'author_flair_text_color': None,
    'permalink': '/r/wow/comments/17tpwfa/15_horse_for_wow_made_more_money_than_starcraft_2/',
    'parent_whitelist_status': 'all_ads',
    'stickied': False,
    'url': 'https://www.reddit.com/r/wow/comments/17tpwfa/15_horse_for_wow_made_more_money_than_starcraft_2/',
    'subreddit_subscribers': 2427761,
    'created_utc': 1699812579.0,
    'num_crossposts': 2,
    'media': None,
    'is_video': False
}
```
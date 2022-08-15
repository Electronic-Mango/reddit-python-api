"""
Module responsible for API itself, registers all blueprints.
"""

from flask import Flask

from api.middleware.authorization import blueprint as authorization
from api.middleware.log_request import blueprint as log_request
from api.sort_type_converter import SortTypeConverter
from api.routes.subreddit.list.all import blueprint as get_subreddit_submissions
from api.routes.subreddit.list.media import blueprint as get_subreddit_media_submissions
from api.routes.subreddit.list.text import blueprint as get_subreddit_text_submissions
from api.routes.subreddit.random.all import blueprint as get_subreddit_random_submission
from api.routes.subreddit.random.media import blueprint as get_subreddit_random_media_submission
from api.routes.subreddit.random.text import blueprint as get_subreddit_random_text_submission
from api.routes.user.list.all import blueprint as get_user_submissions
from api.routes.user.list.media import blueprint as get_user_media_submissions
from api.routes.user.list.text import blueprint as get_user_text_submissions
from api.routes.user.random.all import blueprint as get_user_random_submission
from api.routes.user.random.media import blueprint as get_user_random_media_submission
from api.routes.user.random.text import blueprint as get_user_random_text_submission


def prepare_api() -> Flask:
    """Prepare and configure API, register all blueprints"""
    api = Flask(__name__)
    api.url_map.strict_slashes = False
    api.url_map.converters["sort"] = SortTypeConverter
    api.register_blueprint(log_request)
    api.register_blueprint(authorization)
    api.register_blueprint(get_subreddit_submissions)
    api.register_blueprint(get_subreddit_media_submissions)
    api.register_blueprint(get_subreddit_text_submissions)
    api.register_blueprint(get_subreddit_random_submission)
    api.register_blueprint(get_subreddit_random_media_submission)
    api.register_blueprint(get_subreddit_random_text_submission)
    api.register_blueprint(get_user_submissions)
    api.register_blueprint(get_user_media_submissions)
    api.register_blueprint(get_user_text_submissions)
    api.register_blueprint(get_user_random_submission)
    api.register_blueprint(get_user_random_media_submission)
    api.register_blueprint(get_user_random_text_submission)
    return api

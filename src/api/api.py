"""
Module responsible for API itself, registers all blueprints.
"""

from flask import Flask

from api.before_request import blueprint as before_api_request
from api.routes.subreddit.list.all import blueprint as get_subreddit_submissions
from api.routes.subreddit.list.image import blueprint as get_subreddit_image_submissions
from api.routes.subreddit.list.text import blueprint as get_subreddit_text_submissions
from api.routes.subreddit.random.all import blueprint as get_subreddit_random_submission
from api.routes.subreddit.random.image import blueprint as get_subreddit_random_image_submission
from api.routes.subreddit.random.text import blueprint as get_subreddit_random_text_submission
from api.routes.user.list.all import blueprint as get_user_submissions
from api.routes.user.list.image import blueprint as get_user_image_submissions
from api.routes.user.list.text import blueprint as get_user_text_submissions
from api.routes.user.random.all import blueprint as get_user_random_submission
from api.routes.user.random.image import blueprint as get_user_random_image_submission
from api.routes.user.random.text import blueprint as get_user_random_text_submission


def prepare_api() -> Flask:
    """Prepare and configure API, register all blueprints"""
    api = Flask(__name__)
    api.url_map.strict_slashes = False
    api.register_blueprint(before_api_request)
    api.register_blueprint(get_subreddit_submissions)
    api.register_blueprint(get_subreddit_image_submissions)
    api.register_blueprint(get_subreddit_text_submissions)
    api.register_blueprint(get_subreddit_random_submission)
    api.register_blueprint(get_subreddit_random_image_submission)
    api.register_blueprint(get_subreddit_random_text_submission)
    api.register_blueprint(get_user_submissions)
    api.register_blueprint(get_user_image_submissions)
    api.register_blueprint(get_user_text_submissions)
    api.register_blueprint(get_user_random_submission)
    api.register_blueprint(get_user_random_image_submission)
    api.register_blueprint(get_user_random_text_submission)
    return api

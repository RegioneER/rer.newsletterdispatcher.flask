# -*- coding: utf-8 -*-
from flask import Flask

# from flask_mail import Mail
from flask_mailman import Mail
from flask_restful import Api
from rq import Queue
from routes import routes_bp
from werkzeug.utils import ImportStringError
from sentry_sdk.integrations.flask import FlaskIntegration

import sentry_sdk
import os
import redis
import logging

logger = logging.getLogger(__name__)


def testing_enabled():
    # testing = os.environ.get("TESTING", default="false")
    testing = os.environ.get("TESTING", "false")
    return testing.lower() in {"1", "t", "true"}


def create_app(debug=True):
    """Create an application."""

    app = Flask(__name__)
    logging.basicConfig(
        filename="var/log/newsletter_dispatcher.log",
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
    )
    try:
        app.config.from_object("config.Config")
    except ImportStringError:
        logger.error("No config.py file found. Starting with standard configuration.")

    if app.config.get("SENTRY_DSN", ""):
        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN", ""),
            integrations=[FlaskIntegration()],
            # debug=True,
        )

    app.config["TESTING"] = testing_enabled()
    if app.config.get("REDIS_PORT", ""):
        app.redis = redis.Redis(port=app.config["REDIS_PORT"])
    else:
        app.redis = redis.Redis()
    app.task_queue = Queue(connection=app.redis, default_timeout=10000)
    app.mail = Mail(app)
    Api(routes_bp)
    app.register_blueprint(routes_bp)

    return app

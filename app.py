# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail
from flask_restful import Api
from rq import Queue
from routes import routes_bp
from werkzeug.utils import ImportStringError

import os
import redis
import logging

logger = logging.getLogger(__name__)


def testing_enabled():
    testing = os.environ.get("TESTING", default="false")
    return testing.lower() in {"1", "t", "true"}


def create_app(debug=True):
    """Create an application."""
    app = Flask(__name__)
    logging.basicConfig(
        filename='var/log/newsletter_dispatcher.log',
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
    )
    try:
        app.config.from_object('aconfig.Config')
    except ImportStringError:
        logger.error(
            "No config.py file found. Starting with stadndard configuration."
        )
    app.config['TESTING'] = testing_enabled()

    app.redis = redis.Redis()
    app.task_queue = Queue(connection=app.redis, default_timeout=6000)
    app.mail = Mail(app)
    Api(routes_bp)
    app.register_blueprint(routes_bp)

    return app

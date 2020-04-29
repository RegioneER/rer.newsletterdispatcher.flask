# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail
from flask_restful import Api
from rq import Queue
from routes import routes_bp

import os
import redis
import logging


def testing_enabled():
    testing = os.environ.get("TESTING", default="false")
    return testing.lower() in {"1", "t", "true"}


def create_app(debug=True):
    """Create an application."""
    logging.basicConfig(
        filename='newsletter_dispatcher.log',
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
    )

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg', silent=True)
    app.config['TESTING'] = testing_enabled()
    app.redis = redis.Redis()
    app.task_queue = Queue(connection=app.redis, default_timeout=6000)
    app.mail = Mail(app)
    Api(routes_bp)
    app.register_blueprint(routes_bp)

    return app

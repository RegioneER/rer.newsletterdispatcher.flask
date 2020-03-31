# -*- coding: utf-8 -*-
from flask import Flask
from flask_mail import Mail
from flask_restful import Api
from rq import Queue
from routes import routes_bp
import redis


def create_app(debug=True):
    """Create an application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.cfg', silent=True)

    app.redis = redis.Redis()
    app.task_queue = Queue(connection=app.redis)
    app.mail = Mail(app)
    Api(routes_bp)
    app.register_blueprint(routes_bp)

    return app

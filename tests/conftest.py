# -*- coding: utf-8 -*-
from fakeredis import FakeStrictRedis
from pytest import fixture
from rq import Queue

from app import create_app


@fixture
def app():
    _app = create_app()
    _app.task_queue = Queue(connection=FakeStrictRedis())
    return _app


@fixture
def client(app):
    _client = app.test_client()
    return _client

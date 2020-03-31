# -*- coding: utf-8 -*-
from app import create_app
from pytest import fixture
from fakeredis import FakeStrictRedis
from rq import Queue


@fixture
def app():
    _app = create_app()
    _app.task_queue = Queue(connection=FakeStrictRedis())
    return _app


@fixture
def client(app):
    _client = app.test_client()
    return _client

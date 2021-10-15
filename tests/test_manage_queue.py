# -*- coding: utf-8 -*-
from app import create_app
from fakeredis import FakeStrictRedis
from pytest import fixture
from rq import Queue

EXAMPLE_HTML = (
    "<html><body><h1>Newsletter volume Foo</h1><p>Lorem ipsum</p></body></html>"  # noqa
)

EXAMPLE_PARAMETERS = {
    "channel_url": "http://foo.com",
    "subscribers": ["example-{}@foo.it".format(x) for x in range(100)],
    "subject": "Newsletter vol. Foo",
    "mfrom": "foo@bar.com",
    "send_uid": "asdfghjkl",
    "text": EXAMPLE_HTML,
}


@fixture
def app():
    _app = create_app()
    _app.task_queue = Queue(connection=FakeStrictRedis(), is_async=False)
    return _app


def test_job_executes_correctly(app, requests_mock):

    requests_mock.post("http://foo.com/@send-complete", status_code=204)

    job = app.task_queue.enqueue("tasks.background_task", kwargs=EXAMPLE_PARAMETERS)
    assert job.is_finished

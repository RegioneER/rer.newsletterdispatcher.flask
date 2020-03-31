# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import current_app as app
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource

routes_bp = Blueprint("routes", __name__)
api = Api(routes_bp)

parser = reqparse.RequestParser()
parser.add_argument("_authenticator", type=str, required=True)
parser.add_argument("uid", type=str, required=True)


class AddToQueue(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        job = app.task_queue.enqueue('tasks.background_task', args)
        return {'job_id': job.id, 'date': job.enqueued_at.isoformat()}


api.add_resource(AddToQueue, "/add-to-queue")

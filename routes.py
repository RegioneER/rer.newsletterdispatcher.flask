# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import current_app as app
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask import request

import logging

logger = logging.getLogger("[API]")

routes_bp = Blueprint("routes", __name__)
api = Api(routes_bp)

parser = reqparse.RequestParser()
parser.add_argument("channel_url", type=str, required=True)
parser.add_argument("mfrom", type=str, required=True)
parser.add_argument("send_uid", type=str, required=True)
parser.add_argument("subject", type=str, required=True)
parser.add_argument("subscribers", action="append", required=True)
parser.add_argument("text", type=str, required=True)


class AddToQueue(Resource):
    def post(self):
        params = parser.parse_args(strict=True)
        files = request.files
        if files:
            params["attachments"] = [
                {
                    "content_type": v.content_type,
                    "filename": k,
                    "data": v.read(),
                }
                for k, v in files.items()
            ]
        job = app.task_queue.enqueue(
            "tasks.background_task",
            kwargs=params,
            job_timeout=len(params["subscribers"]) * 5,
        )
        logger.info(
            'Add to queue "{subject}" for {subscribers} subscribers.'.format(
                subject=params["subject"],
                subscribers=len(params["subscribers"]),
            )
        )
        return {"job_id": job.id, "date": job.enqueued_at.isoformat()}


api.add_resource(AddToQueue, "/add-to-queue")

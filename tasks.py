# -*- coding: utf-8 -*-
from app import create_app
from flask_mail import Message

import requests

app = create_app()
app.app_context().push()


def retrieve_message_infos(channel_url, message_id):
    import pdb

    pdb.set_trace()


def background_task(
    channel_url, text, subscribers, subject, mfrom, _authenticator
):
    """ Function that returns len(n) and simulates a delay """
    with app.mail.connect() as conn:
        for mto in subscribers:
            msg = Message(
                recipients=[mto],
                html=text,
                subject=subject,
                sender=mfrom,
                charset='utf-8',
            )
            conn.send(msg)

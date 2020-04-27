# -*- coding: utf-8 -*-
from app import create_app
from flask_mail import Message

import logging
import requests

app = create_app()
app.app_context().push()


logger = logging.getLogger('[SEND COMPLETE]')


def background_task(
    channel_url, text, subscribers, subject, mfrom, _authenticator, send_uid
):
    """ Function that returns len(n) and simulates a delay """
    with app.mail.connect() as conn:
        for i, mto in enumerate(subscribers):
            msg = Message(
                recipients=[mto],
                html=text,
                subject=subject,
                sender=mfrom,
                charset='utf-8',
            )
            conn.send(msg)
            logger.info('[{}/{}] - {}'.format(i + 1, len(subscribers), mto))
    requests.post(
        '{}/@send-complete'.format(channel_url),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        json={'send_uid': send_uid},
    )
    logger.info(
        'Sent "{subject}" to {subscribers} recipients through channel "{channel}".'.format(  #  noqa
            subject=subject, subscribers=len(subscribers), channel=channel_url
        )
    )

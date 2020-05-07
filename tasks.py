# -*- coding: utf-8 -*-
from app import create_app
from flask_mail import Message

import logging
import requests

app = create_app()
app.app_context().push()


logger = logging.getLogger('[QUEUE]')


def background_task(channel_url, text, subscribers, subject, mfrom, send_uid):
    """ Function that returns len(n) and simulates a delay """
    logger.info(
        'Start send "{subject}" to {subscribers} recipients through channel "{channel}".'.format(  #  noqa
            subject=subject, subscribers=len(subscribers), channel=channel_url
        )
    )
    try:
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
                # logger.debug(
                #     '[{}/{}] - {}'.format(i + 1, len(subscribers), mto)
                # )
    except ConnectionRefusedError as e:
        logger.error('Message not sent:')
        logger.exception(e)
        requests.post(
            '{}/@send-complete'.format(channel_url),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            json={'send_uid': send_uid, 'error': True},
        )
        return
    res = requests.post(
        '{}/@send-complete'.format(channel_url),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        json={'send_uid': send_uid},
    )
    if res.code != 204:
        logger.error(
            'Unable to update date to remote: {code} - {reason}'.format(
                code=res.code, reason=res.reason
            )
        )
    logger.info('Task complete.')

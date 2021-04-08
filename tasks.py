# -*- coding: utf-8 -*-
from app import create_app
from flask_mail import Message
from smtplib import SMTPRecipientsRefused

import logging
import requests

app = create_app()
app.app_context().push()


logger = logging.getLogger("[QUEUE]")


def background_task(
    channel_url, text, subscribers, subject, mfrom, send_uid, attachments=[]
):
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
                    charset="utf-8",
                )
                for attachment in attachments:
                    msg.attach(
                        filename=attachment.get("filename", ""),
                        data=attachment.get("data", ""),
                        content_type=attachment.get("content_type", ""),
                    )
                try:
                    conn.send(msg)
                except SMTPRecipientsRefused:
                    logger.info("[SKIP] - {}: invalid address.".format(mto))
                if (i + 1) % 1000 == 0:
                    logger.info(
                        "- Sending status: {}/{}".format(
                            i + 1, len(subscribers)
                        )
                    )
    except Exception as e:
        logger.error("Message not sent:")
        logger.exception(e)
        requests.post(
            "{}/@send-complete".format(channel_url),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={"send_uid": send_uid, "error": True},
        )
        return
    res = requests.post(
        "{}/@send-complete".format(channel_url),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={"send_uid": send_uid},
    )
    if res.status_code != 204:
        logger.error(
            'Unable to update date to remote: received "{code}" instead a "204".'.format(  #  noqa
                code=res.status_code
            )
        )
    logger.info("Task complete.")

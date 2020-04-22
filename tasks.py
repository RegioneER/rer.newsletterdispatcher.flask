# -*- coding: utf-8 -*-
from app import create_app
from flask_mail import Message

app = create_app()
app.app_context().push()


def background_task(
    channel_url, text, subscribers, subject, mfrom, _authenticator, send_uid
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

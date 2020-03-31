# -*- coding: utf-8 -*-
from app import create_app
from flask_mail import Message

app = create_app()
app.app_context().push()


def background_task(parameters):

    """ Function that returns len(n) and simulates a delay """
    with app.mail.connect() as conn:
        for x in range(100):
            email = 'example-{}@foo.it'.format(x)
            message = '...'
            subject = 'hello, %s' % email
            msg = Message(recipients=[email], body=message, subject=subject)
            conn.send(msg)

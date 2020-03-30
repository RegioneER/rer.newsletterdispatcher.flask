from flask import Flask
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
mail = Mail(app)

mails = ['aaa@gmail.com', 'bbb@gmail.com']


@app.route("/")
def index():

    with mail.connect() as conn:
        print "Inizio la spedizione"
        for x in range(70000):
            email = 'ciccio-{}@qualcosa.it'.format(x)
            print email
            message = '...'
            subject = "hello, %s" % email
            msg = Message(
                sender="from@example.com",
                recipients=[email],
                body=message,
                subject=subject,
            )

            conn.send(msg)
        print "Finita"

from flask_mail import Message
from flask import current_app

from .app import mail


def send_email(to, subject, template):
    with current_app.app_context():
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)

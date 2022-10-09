import threading
from threading import Thread

from django.core.mail import send_mail

from config.settings.base import env

EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="sample_email_host_user")


class EmailThread(Thread):
    def __init__(self, from_email, subject, html_message, message, neis_email):
        self.from_email = from_email
        self.subject = subject
        self.recipient_list = neis_email
        self.html_message = html_message
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        data = {
            "from_email": self.from_email,
            "recipient_list": [self.recipient_list],
            "subject": self.subject,
            "message": self.message,
            "html_message": self.message,
        }
        send_mail(**data)

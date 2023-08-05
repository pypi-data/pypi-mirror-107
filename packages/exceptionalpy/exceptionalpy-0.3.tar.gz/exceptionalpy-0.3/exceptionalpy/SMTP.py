from smtplib import SMTP_SSL
from smtplib import SMTP
from email.mime.text import MIMEText

from exceptionalpy import BaseNotifier, Handler


class SMTPNotifier(BaseNotifier):
    _cls = SMTP

    def __init__(self, address: tuple, sender: str, credentials: tuple, destinations: list[str],
                 subject: str):
        BaseNotifier.__init__(self)
        self.address = address
        self.sender = sender
        self.credentials = credentials
        self.destinations = destinations
        self.subject = subject

    def send(self, data: dict):
        msg = '\n'.join(data)  # todo: fix
        msg = MIMEText(msg, "plain")
        msg["Subject"] = self.subject
        msg["From"] = self.sender

        print("Connecting to server")
        with self._cls(self.address[0], self.address[1]) as c:
            if self.credentials:
                c.login(self.credentials[0], self.credentials[1])
            print("Sending email")
            c.sendmail(self.sender, self.destinations, msg.as_string())
            c.quit()


class SMTPSNotifier(SMTPNotifier):
    _cls = SMTP_SSL


class SMTPHandler(Handler):
    _cls = SMTPNotifier

    def __init__(self, address: tuple, sender: str, destinations: list[str], subject: str,
                 init: bool = True, credentials: tuple = None):
        Handler.__init__(self, init)
        self._notifier = self._cls(address, sender, credentials, destinations, subject)


class SMTPSHandler(SMTPHandler):
    _cls = SMTPSNotifier

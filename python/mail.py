import smtplib
import ssl
from copy import deepcopy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    def __init__(self, sender, password, port=587):
        self.port = port
        self.sender = sender
        self.password = password
        self.msg = MIMEMultipart()
        self.msg["Subject"] = "Feedback"
        self.msg["From"] = sender

    def send(self, receivers, messages):
        global server
        msg = deepcopy(self.msg)
        msg['To'] = ", ".join(receivers)
        print(msg)
        msg.attach(MIMEText(messages))
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP("smtp.gmail.com", self.port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, receivers, msg.as_string())

        except Exception as e:
            # Print any error messages
            print(e)
        finally:
            server.quit()

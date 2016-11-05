import sendgrid
import os


class SendGrid:
    client = None

    def __init__(self):
        self.client = sendgrid.SendGridClient(os.environ["send_grid_api_key"])

    def sendMail(self, to_email, name):
        message = sendgrid.Mail()
        message.add_to(to_email)
        message.set_from("raulguti90@gmail.com")
        message.set_subject('Your video have been processed')
        message.set_html("""
        Hello, """+name+"""

        Your video is already Available on the contest's site.
        Thank you for your participation!""".encode('utf-8'))

        self.client.send(message)
from .email_service import set_email_format, send_email
import os
from settings import REPORT_PROCESSED
from robot import PATH


def send_message(recipients=None):
    """
    Sends an e-mail message with the recipients arguments and EMAIL_RECIPIENTS as recipients and inserting the file specified by filename as attachment.
    """
    files = [os.path.join(PATH, 'attachments', file)
             for file in os.listdir(os.path.join(PATH, 'attachments'))]
    files.append(os.path.join(PATH, REPORT_PROCESSED))
    message = set_email_format(recipients, files_to_attach=files)
    send_email(message)

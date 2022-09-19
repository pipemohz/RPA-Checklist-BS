import logging
import email
import imaplib
from os.path import join
import datetime as dt
from robot import PATH
from settings import SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, REPORT_NAME, SUBJECT


def download_all_attachments(conn: imaplib.IMAP4_SSL, email_id: bytes, path=PATH):
    """
    Download all files attached in message.
    """

    typ, data = conn.fetch(email_id, '(RFC822)')
    email_body = data[0][1]
    mail = email.message_from_bytes(email_body)
    if mail.get_content_maintype() != 'multipart':
        return
    for part in mail.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            open(join(path, REPORT_NAME),
                 'wb').write(part.get_payload(decode=True))


def connect_to_mailbox():
    """
    Stablish a connection with mailbox, search all messages with defined subject and download all files attached to message.
    """
    today = dt.datetime.now()
    logging.info("Executing module mailbox")

    with imaplib.IMAP4_SSL(SMTP_HOST) as conn:
        conn.login(SMTP_USERNAME,
                   password=SMTP_PASSWORD)
        conn.select(readonly=False)
        # Using search method to filter messages by subject (SUBJECT ""), date (ON) and unseen (USEEN).
        data = conn.search(None, f'(SUBJECT "{SUBJECT}"',
                           f'ON {today.strftime("%d-%b-%Y")}', 'UNSEEN)')[1]
        emails_id = [_id.decode('utf8') for _id in data[0].split()]

        if emails_id:
            for _id in emails_id:
                download_all_attachments(conn, _id)
                conn.store(_id, '+FLAGS', r'(\Seen)')

            logging.info("Report downloaded from mailbox successfully.")
        else:
            logging.error("Report was not found in mailbox.")

import logging
from robot.manage_directories import create_directories
from settings import LOG_NAME

# Create project directories
PATH = create_directories()


def main():
    from .mailbox import connect_to_mailbox
    from .browser import browsing_session
    from .processing import process_report
    from .email import send_message

    logging.basicConfig(filename=LOG_NAME, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info("Robot started.")

    # Execute mailbox_service module
    connect_to_mailbox()
    logging.info("Mailbox module finished.")
    # Execute browsing_session module
    browsing_session()
    logging.info("Browsing module finished.")
    # Execute process_report module
    process_report()
    logging.info("Processing module finished.")
    # Execute email module.
    send_message()
    logging.info("Email module finished.")

    logging.info("Robot finished.")

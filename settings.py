from dotenv import load_dotenv
from datetime import datetime, timedelta
import pathlib
import os

load_dotenv('.env')

# Mailbox settings
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

# Subject of emails to get form mailbox
SUBJECT = os.environ.get('SUBJECT')

# Subject of email message report to send
MESSAGE_SUBJECT = os.environ.get('MESSAGE_SUBJECT').replace(
    '$(fecha_ayer)', f'{(datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")}')


# Email message template
with open(os.environ.get('MESSAGE_FILE'), mode='r', encoding='utf8') as f:
    MESSAGE = """"""
    for line in f.readlines():
        MESSAGE += line

# List of email recipients to send notifications.
EMAIL_RECIPIENTS = os.environ.get('EMAIL_RECIPIENTS')

# Carbon copy recipients
CC = os.environ.get('CC')

# Project settings
# BASE_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = os.path.dirname(__file__)

# File settings
# Folder to storage reports downloaded from Cloudfeet
FILES_DIR = os.environ.get('FILES_DIR')
# File name of checklist report dowloaded from Cloudfeet
CHECKLIST_NAME = os.environ.get('CHECKLIST_NAME')
# File name of report from Geotab
REPORT_NAME = os.environ.get('REPORT_NAME')
# File name of report after processing.
REPORT_PROCESSED = os.environ.get('REPORT_PROCESSED')
# Stats file
STATS_REPORT = 'stats.xlsx'


# Logging settings
LOG_NAME = os.environ.get('LOG_NAME')

# Web browser settings
# Browser engine
CHROME_DRIVER_PATH = r"C:\chrome_driver\chromedriver.exe"
# Maximum time to wait for a download to complete
MAX_TIME = 10

# Navigation session
CLOUDFEET_URL = os.environ.get('CLOUDFEET_URL')
# Cloudfeet user credentials
CLOUDFEET_USERNAME = os.environ.get('CLOUDFEET_USERNAME')
CLOUDFEET_PASSWORD = os.environ.get('CLOUDFEET_PASSWORD')

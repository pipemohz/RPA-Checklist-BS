# Botero-Soto checklist RPA

App for building a table with data from countries and save it to a json file and sqlite database. It retrieves data from [Rest Countries API](https://restcountries.com/) and builds a pandas dataframe. Each row contains country region, country name, an encrypted version of country language in SHA1 and time elapsed in building row.

RPA for automating the checklist processing of Botero-Soto enterprise. First, it downloads reports sent automatically from GeoTab platform from mailbox. Second, the robot creates a web browsing session for downloading checklist report from Cloudfleet. With both reports, the robot builds a consolidated report and these will be send to members of Botero-Soto organization. The application implements Selenium and Pandas frameworks and uses smtplib and imaplib Python libraries.


## Installation 🔧

Clone the repository in a your work folder.

## Configuration

### Create a virtual environment
```
python -m venv .venv
```
### Activate virtul environment

#### Windows
```
.venv\Scripts\activate
```
#### Linux
```
source .venv/bin/activate
```
### Download all packages required
```
pip install -r requirements.txt
```
### Create an environment file

You must create a .env file for project configuration. It must contain following variables:

```
##################
# LOGGING SETTINGS
##################

LOG_NAME=task.log

##################
# FILE SETTINGS
##################

# Folder to storage reports downloaded from Cloudfeet
FILES_DIR=reports
# File name of checklist report dowloaded from Cloudfeet
CHECKLIST_NAME=28592_Checklist
# File name of report from Geotab
REPORT_NAME=INFORME REALIZACIÓN CHECKLIST SIN PROCESAR.xlsx
# File name of report after processing
REPORT_PROCESSED=INFORME REALIZACIÓN CHECKLIST PREOPERACIONAL.xlsx

###################
# MAILBOX SETTINGS
###################

SMTP_HOST=domain_of_mail_server
SMTP_PORT=port_number
SMTP_USERNAME=your_email_account
SMTP_PASSWORD=your_email_password

# Subject of emails to get form mailbox
SUBJECT=Scheduled report on database sytprodes: CHECKLIST PREOPERACIONAL DIARIO
# SUBJECT=Reporte programado en la base de datos sytprodes: INFORME

# Email message template file
MESSAGE_FILE=message.txt

# Subject of email message report to send
MESSAGE_SUBJECT=Checklist Pre operacional cumplimiento $(fecha_ayer)

# List of email recipients to send notifications
EMAIL_RECIPIENTS=email1@mail.com,email2@mail.com
# Carbon copy recipients
CC=ccemail1@mail.com,ccemail2@mail.com

#######################
# WEB BROWSER SETTINGS
#######################

CLOUDFEET_URL=https://fleet.cloudfleet.com/Ingreso/
CLOUDFEET_USERNAME=your_cloudfleet_username
CLOUDFEET_PASSWORD=your_cloudfleet_password

```
### Create a body email message file called message.txt with a custom text

## Running tests

## Run app
```
python run.py
```

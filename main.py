#!.venv/bin/python3
import pdfkit
import os
from imap_tools import MailBox
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

IMAP_SERVER = os.getenv('IMAP_SERVER')
IMAP_USER = os.getenv('IMAP_USER')
IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')
IMAP_FOLDER = os.getenv('IMAP_FOLDER')
SAVE_DIRECTORY = os.getenv('SAVE_DIRECTORY')
PULL_FREQUENCY = int(os.getenv('PULL_FREQUENCY'))

print(f'{datetime.datetime.now()} - Initializing')


def processEmails():
    print(f'{datetime.datetime.now()} - Connecting to server {IMAP_SERVER}')
    with MailBox(IMAP_SERVER).login(IMAP_USER, IMAP_PASSWORD, IMAP_FOLDER) as mailbox:
        for i, msg in enumerate(mailbox.fetch('UNSEEN', limit=10)):
            print(
                f'{datetime.datetime.now()} - Processing email with subject {msg.subject}')
            filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            save_target = f'{SAVE_DIRECTORY}/{filename}.pdf'
            pdf_options = {
                'title': msg.subject
            }
            html = '<meta http-equiv="Content-type" content="text/html; charset=utf-8"/>' + \
                msg.html
            pdfkit.from_string(html, save_target, pdf_options)


sched = BlockingScheduler()
start = datetime.datetime.now() + datetime.timedelta(0, 30)

# Schedule processEmails to be called every PULL_FREQUENCY seconds
sched.add_job(processEmails, 'interval',
              seconds=PULL_FREQUENCY, start_date=start)
sched.start()

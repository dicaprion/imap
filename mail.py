import base64
import datetime
import email
from email.header import decode_header
import os
from email import errors
import imap
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from numpy import unicode
from io import StringIO
from collections import defaultdict


def get_all_messages(login, password, port, host):
    global local_message_date
    EMAIL_ACCOUNT = login
    PASSWORD = password

    mail = imap.IMAP4_SSL(port, host)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "ALL")
    i = len(data[0].split())
    result_list = list()
    dictionary = defaultdict()
    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('cp1256')
        email_message = email.message_from_string(raw_email_string)

        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            global local_message_date
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        body = parse(email_message)
        result_list.append((email_from, local_message_date, subject, body))
        dictionary['(' + str(x) + ',' + ')'] = email_message

    mail.close()
    mail.logout()
    return result_list, dictionary


def get_attachments(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        dh = decode_header(part.get_filename())

        default_charset = 'ASCII'
        fileName = ''.join([unicode(t[0], t[1] or default_charset) for t in dh])
        if bool(fileName):
            filePath = os.path.join('', fileName)
            with open(filePath, 'wb') as f:
                f.write(part.get_payload(decode=True))


def parse(message):
    body = ''
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            if part.get_content_charset() is not None:
                body += unicode(part.get_payload(decode=True), errors='ignore')
    return body


def send_message(message, login, password, target, subject):
    fromaddr = login
    toaddr = target
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

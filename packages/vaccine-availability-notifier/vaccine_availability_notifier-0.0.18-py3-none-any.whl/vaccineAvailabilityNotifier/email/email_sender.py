import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(res, sender_email_id, sender_email_password, receiver_email_id):
    mail_content = '''Hell there vaccine is available , please book asap ...\n
    https://www.cowin.gov.in/home\n..\n\n'''
    mail_content = mail_content + "\n\n\n" + res
    mail_content = mail_content + "\n\n\nThank you \nNandkishor bhasker"
    # The mail addresses and password
    sender_address = sender_email_id
    sender_pass = sender_email_password
    receiver_address = receiver_email_id

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = '[Important ] Hurry !!!  Vaccines are available...'  # The subject line
    # The body and the attachments for the mail
    _send(message, mail_content, sender_address, sender_pass, receiver_address)
    print('Mail Sent')


def send_email_switch(sender_email_id, sender_email_password, receiver_email_id):
    mail_content = '''Please switch wifi'''
    mail_content = mail_content + "\n\n\nThank you \nNandkishor bhasker"
    # The mail addresses and password
    sender_address = sender_email_id
    sender_pass = sender_email_password
    receiver_address = receiver_email_id
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = '[Important ] Hurry !!!  Please switch wifi...'  # The subject line
    # The body and the attachments for the mail
    _send(message, mail_content, sender_address, sender_pass, receiver_address)
    print('switch email Sent')


def _send(message, mail_content, sender_address, sender_pass, receiver_address):
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.ehlo()
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


def send_email_switch(sender_email_id, sender_email_password, receiver_email_id):
    mail_content = '''Please switch wifi'''
    mail_content = mail_content + "\n\n\nThank you \nNandkishor bhasker"
    # The mail addresses and password
    sender_address = sender_email_id
    sender_pass = sender_email_password
    receiver_address = receiver_email_id

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = '[Important ] Hurry !!!  Please switch wifi...'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.ehlo()
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('switch email Sent')

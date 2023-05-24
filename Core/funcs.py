import re

import environ
from django.template.loader import render_to_string


def int_decrease_by_percentage(num: int, percent: int) -> int:
    return round(num - (num / 100 * percent)) if percent != 0 else num


def EMAIL_validator(email: str, min_len: int = 1, max_len: int = 200) -> bool:
    res = re.match(r'[A-Z0-9a-z.]+@+[A-Z0-9a-z]+[.]+[A-Z0-9a-z]+', email)
    if (res is not None and
            len(res.group(0)) == len(email) and
            min_len <= len(res.group(0)) <= max_len):
        return True
    else:
        return False


def send_EMail(port: int, to: str, subject: str, html: str):
    env = environ.Env()
    server = 'smtp.timeweb.ru'
    user = env('EMAIL_HOST_USER')
    password = env('EMAIL_HOST_PASSWORD')

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from platform import python_version

    sender = user
    subject = subject
    text = 'Something go wrong'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, to, msg.as_string())
    mail.quit()


def send_email_by_template(subject: str, to_email: str, template: str, context: dict = {}, ):
    html_content = str(render_to_string(template, context=context))
    send_EMail(25, to_email, subject, html_content)


ALPHABETS = {
    'en': 'abcdefghijklmnopqrstuvwxyz',
    'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
}


def random_str(length: int = 10, alphabet: str = ALPHABETS['en'], repete: bool = True, upper: bool = True,
               digits: bool = True):  # ru #digits
    import random

    if alphabet == 'ru':
        alphabet = ALPHABETS['ru']
    if alphabet == 'en' or alphabet == 'eu':
        alphabet = ALPHABETS['en']

    if digits:
        alphabet += '0123456789'

    if repete:
        rand_str = ''.join(random.choice(alphabet) for i in range(length))
    else:
        try:
            rand_str = ''.join(random.sample(alphabet, length))
        except ValueError:
            return "The alphabet is less than the length of the string. Generation without repetition is impossible."
    if upper:
        return rand_str.upper()
    else:
        return rand_str

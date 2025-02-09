import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import logging.config
from read_conf import setup_logging


def send_email(subject, body, to_email):
    # スクリプト名を取得
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    setup_logging(script_name)

    logger = logging.getLogger(__name__)
    logger.info("*** Start sending email ***")

    from_email = 'kazuyoshi.hayase@gmail.com'
    from_password = os.getenv('GMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        logger.info(f'Email sent to {to_email}')
    except Exception as e:
        logger.info(f'Failed to send email: {e}')

# 通知を送信
send_email('Process Completed', 'The processing of files is complete.', 'kazuyoshi.hayase@jcom.home.ne.jp')

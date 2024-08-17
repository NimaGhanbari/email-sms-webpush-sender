import os
import smtplib,ssl
from email.mime.text import MIMEText
import logging
from django.core.mail import send_mail
import logging
from celery.task import task
from kavenegar import *

from rest_framework import status
from apps.aaj_farm.utils.monitoring import save_image_and_thumbnail
from rest_framework.response import Response
from celery import shared_task
from django.contrib.auth.models import User
from apps.store.models.advertisement.base_advertisement_model import BaseAdvertisement
from apps.wanted.models.new_requirements.base_requirement_model import BaseRequirement
import logging
from celery.task import task
from kavenegar import *

from apps.aaj_core.utils.web_push import send_web_push
from apps.base.models.sms_log_model import SmsLog
from apps.base.models.web_push_log_model import WebPushLog
from apps.aaj_farm.models.cultivationModel import Cultivation
from rest_framework import status
from apps.aaj_farm.utils.monitoring import save_image_and_thumbnail
from rest_framework.response import Response
from celery import shared_task
from django.contrib.auth.models import User
from apps.store.models.advertisement.base_advertisement_model import BaseAdvertisement
from apps.wanted.models.new_requirements.base_requirement_model import BaseRequirement



def send_verification_email(sender_email, sender_password, recipient_email, subject, body):
    """Sends an email using SMTP protocol.

    Args:
        sender_email: Email address of the sender.
        sender_password: Password for the sender's email account.
        recipient_email: Email address of the recipient.
        subject: Subject line of the email.
        body: Content of the email (plain text).

    Returns:
        True if email is sent successfully, False otherwise.
    """
    logging.info("Try to send Mail")
    message = MIMEText(body, 'plain')
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    
    try:
       
        with smtplib.SMTP('mail.mazraeapp.com',587) as server:
            logging.info("Connecting to the SMTP server")
            server.starttls()  # Secure the connection
            logging.info("Starting TLS")
            server.login(sender_email, sender_password)
            logging.info("Login successful")
            server.sendmail(sender_email, recipient_email, message.as_string())
            logging.info("Email sent successfully")
            return True
    except smtplib.SMTPException as e:
        logging.error(f"Error sending email: {e}")
        return False
    





@task()
def sms_sender_task(message, phone, type,sender_id=None,advertisement_id=None,ad_type=None):
    data = {
        "phone": phone,
        "message": message,
        "type": type
    }
    
    type_model_field = {
        "advertisement": "advertisement_promoted",
        "requirement": "requirement_promoted"
    }
    
    type_model = {
        "advertisement": BaseAdvertisement,
        "requirement": BaseRequirement
    }
    
    if ad_type:
        advertisement = type_model[ad_type].objects.filter(id=advertisement_id).first()
        data[type_model_field[ad_type]] = advertisement
    
    if sender_id:
        sender_user = User.objects.filter(id=sender_id).first()
        data["sender_promotion"] = sender_user
    
    sms_log = SmsLog.objects.create(**data)
    
    try:
        api = KavenegarAPI(
            '395131494D3642383133495A795A337862534B5166644B69615631524F39367463386C7761693170792B733D')
        params = {
            'sender': '90003723',
            'receptor': phone,  # multiple mobile number, split by comma
            'message': message+ '\n' + 'لغو 11',
        }
        response = api.sms_send(params)
        print(response)
        
        sms_log.sender=params['sender']
        sms_log.message_id=str(response[0]['messageid'])
        sms_log.status=str(response[0]['status'])
        sms_log.status_text=response[0]['statustext']
        
        is_send_list_value = [1, 2, 4, 5] # az site kavenegar
        if response[0]['status'] in is_send_list_value:
            sms_log.is_sent=True
        
        sms_log.save()        
        return response
    except APIException as e:
        print(e)
        return e
    except HTTPException as e:
        print(e)
        return e
    except Exception as e:
        return e






@task()
def web_push_notification_task(subscription_information, message_body, app, username):
    if subscription_information is None:
        logging.warning("user fcm token is none")
        return
    
    message = json.loads(str(message_body).replace("'", '"'))
    webpush = WebPushLog.objects.create(
        title=message['title'],
        message=message['body'],
        url=message['url'],
        app=app,
        username=username
    )

    try:
        data = {
            'title': webpush.title,
            'body': webpush.message,
            'url': webpush.url,
            'guid': str(webpush.guid),
        }
        data = str(data).replace("'", '"')
        print(data)
        send_web_push(subscription_information, data)
        webpush.is_sent = True
        webpush.save()
    except Exception as e:
        logging.error(e)
        return

    return 






from pywebpush import webpush, WebPushException

VAPID_PRIVATE_KEY = "NhFFL81NOyqCp97vyxsc9t6p3aetLq3Df72RwmreCTM"
VAPID_PUBLIC_KEY = "BO60T_oiPYcjRST9Dkppg-R69kEoLjSZliLw0EvTwAof6IdU8v-7c4ROpG16LPG0fsoGH7k_gvXGBjnyxvEov2c"

VAPID_CLAIMS = {
    "sub": "mailto:mazreatech@gmail.com"
}


def send_web_push(subscription_information, message_body):
    return webpush(subscription_info=subscription_information,
                   data=message_body,
                   vapid_private_key=VAPID_PRIVATE_KEY,
                   vapid_claims=VAPID_CLAIMS)





# Url کامل باید فرستاده شود تا فرانت وقتی ککاربر روی وب پوش کلیک کرد اون url رو باز کنه البته همه جوره میتوان هندل کرد با فرانت
# vapid ها خودمون دستی ست میکنیم چزی که گفتن مطمِن نیستم

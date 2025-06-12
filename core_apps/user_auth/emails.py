from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger


def sendOTPEmail(recipient_email, otp):
    subject = _('Your OTP code for login')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list =[recipient_email]
    context ={
        "otp":otp,
        "expiry_time": settings.OPT_EXPIRATION,
        "site_name":settings.SITE_NAME,
    }
    html_email = render_to_string("email/otp_email.html", context)
    plain_email= strip_tags(html_email)
    message = EmailMultiAlternatives(subject , plain_email , from_email, recipient_list)
    message.attach_alternative(html_email, "text/html")
    try:
        message.send()
        logger.info(f"OTP email send successfully to: {recipient_email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {recipient_email}: Error {str(e)}")

def sendAccountLockedEmail(user):
    subject = _('Your Account has been locked')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list =[user.email]
    context ={
        "user":user,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds()//60),
        "site_name":settings.SITE_NAME,
    }
    html_email = render_to_string("email/account_email.html", context)
    plain_email= strip_tags(html_email)
    message = EmailMultiAlternatives(subject , plain_email , from_email, recipient_list)
    message.attach_alternative(html_email, "text/html")
    try:
        message.send()
        logger.info(f"Account locked email send successfully to: {user.email}")
    except Exception as e:
        logger.error(f"Failed to send account locked email to {user.email}: Error {str(e)}")
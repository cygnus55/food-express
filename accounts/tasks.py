from celery import shared_task

from django.core.mail import EmailMessage

@shared_task
def activate_account_email_task(message, to_email):
    """
        task to send an email-notification when an account is newly registered.
    """
    mail_subject = 'Activate your Food Express account.'
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
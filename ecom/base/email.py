from django.conf import settings
from django.core.mail import send_mail




def send_account_activation_email(email, email_token):
    subject = 'Activate your account'
    email_from = settings.EMAIL_HOST_USER
    content = f'Hello {email}, Please click on the link below to activate your account'
    link = f'http://localhost:8000/account/activate/{email_token}'
    message = content + f'\n\n{link}'

    send_mail(subject, message, email_from, [email])

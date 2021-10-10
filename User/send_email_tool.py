from User.models import EmailVertifyCode
from random import choice

from django.core.mail import send_mail
from e_commerce.settings import EMAIL_FROM


def get_random_code(code_length):
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        # select a character randomly
        code += choice(code_source)
        return code

def send_email_code(email,send_type):
    # first: create email verification code object，save the database, and use it for comparison later
    code = get_random_code(6)
    a = EmailVertifyCode()
    a.email = email
    a.send_type = send_type
    a.code = code
    a.save()
    #second:
    send_title = ''
    send_body = ''
    if send_type == 1:
        send_title = "Register the Aoligei!"
        send_body = 'Please click the link below to activate your account:\n http://127.0.0.1:8000/'+code
        send_mail(send_title,send_body,EMAIL_FROM,[email])

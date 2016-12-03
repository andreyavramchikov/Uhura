from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_confirmation_email():
    title = u'Order Confirmation Email'
    msg_plain = render_to_string('email/order_confirmation_email.txt', {'data': ''})
    msg_html = render_to_string('email/order_confirmation_email.html', {'data': ''})
    send_mail(
        title,
        msg_plain,
        'aldrson2@gmail.com',
        ['aldrson2@gmail.com'],
        html_message=msg_html,
    )

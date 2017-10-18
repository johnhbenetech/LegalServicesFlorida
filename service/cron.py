import kronos
import os
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template
from django.template import Context
from .models import ServiceUpdate

@kronos.register('*/1 * * * *')
def send_service_updates_emails():
    print("RUNNING")
    
    
    if os.environ.get('DJANGO_EMAIL_SUBJECT') and os.environ.get('DJANGO_EMAIL_FROM') and os.environ.get('DJANGO_EMAIL_TO'):
        subject = os.environ.get('DJANGO_EMAIL_SUBJECT')
        from_email = os.environ.get('DJANGO_EMAIL_FROM')
        to = os.environ.get('DJANGO_EMAIL_TO').split(',')
    else:
        subject = "Test Email Subject"
        from_email = 'notifications@accountmail.co'
        to = ['johnh@benetech.org',]

    service_updates = ServiceUpdate.objects.filter(is_emailed=False)

    print(service_updates)
    
    html_template = get_template('service/email/service_updates.html')
    text_template = get_template('service/email/service_updates.txt')
    context = {'service_updates': service_updates}

    text_content = text_template.render(context)
    html_content = html_template.render(context)

    
    if service_updates:
        connection = get_connection()
        connection.open()
    
        msg = EmailMultiAlternatives(subject, text_content, from_email, to, connection=connection)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
        for service_update in service_updates:
            service_update.is_emailed = True
            service_update.save()

import kronos
import os
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template
from django.template import Context
from .models import ProviderUpdate

@kronos.register('0 2 * * 0')
def send_provider_updates_emails():
    subject = os.environ.get('DJANGO_EMAIL_SUBJECT')
    from_email = os.environ.get('DJANGO_EMAIL_FROM')
    to = os.environ.get('DJANGO_EMAIL_TO').split(',')

    provider_updates = ProviderUpdate.objects.filter(is_emailed=False)

    html_template = get_template('provider/email/provider_updates.html')
    text_template = get_template('provider/email/provider_updates.txt')
    context = {'provider_updates': provider_updates}

    text_content = text_template.render(context)
    html_content = html_template.render(context)

    connection = get_connection()
    connection.open()

    msg = EmailMultiAlternatives(subject, text_content, from_email, to, connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    for provider_update in provider_updates:
        provider_update.is_emailed = True
        provider_update.save()

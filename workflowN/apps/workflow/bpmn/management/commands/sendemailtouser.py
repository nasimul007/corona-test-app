import json
import logging

from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
import html
from django.db import transaction
from apps.workflow.bpmn.models import Delegation, AppComment, EmailQueues, FailedEmailQueues
from django.template.loader import render_to_string

from conf import licensed


class Command(BaseCommand):
    help = 'Send email by scheduler'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        connection = get_connection(host=licensed.EMAIL_HOST, port=licensed.EMAIL_PORT,
                                    username=licensed.EMAIL_HOST_USER,
                                    password=licensed.EMAIL_HOST_PASSWORD, use_tls=licensed.EMAIL_USE_TLS)
        try:
            connection.open()
            pending_emails = EmailQueues.objects.filter(status=False).order_by('-id')[
                             :licensed.EMAIL_SEND_LIMIT_AT_ONE_BATCH]
            for email in pending_emails:
                try:
                    # send mail to user
                    subject, from_email, to, cc = email.subject, email.from_e, email.to, email.cc
                    text_content = html.unescape(email.body)
                    html_content = html.unescape(email.body)

                    if to:
                        try:
                            to = eval(to)
                        except Exception as e:
                            to = [to]
                    else:
                        to = []

                    if cc:
                        try:
                            cc = eval(cc)
                        except Exception as e:
                            cc = [cc]
                    else:
                        cc = []

                    msg = EmailMultiAlternatives(
                        subject=subject, body=text_content, from_email=from_email, to=to,
                        cc=cc, connection=connection)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    # write log if success
                    logger = logging.getLogger('success_logger')
                    logger.warning('Mail sent to {} is done.'.format(to))

                    # change the email status for future
                    email.status = True
                    email.save()
                    email.attempt = email.attempt + 1
                    email.save()
                    print("mail sent")
                except Exception as e:
                    # Write log
                    print("mail sent fail. please check error log")
                    logger = logging.getLogger('warning_logger')
                    logger.error('{}'.format(e.__str__()))

                    email.attempt = email.attempt + 1
                    email.save()
                    if email.attempt >= licensed.EMAIL_SEND_ATTEMPT_TIMES:
                        with transaction.atomic():
                            fail_email = FailedEmailQueues(from_e=email.from_e, to=email.to, cc=email.cc,
                                                           subject=email.subject,
                                                           body=email.body, attempt=email.attempt)
                            fail_email.save()
                            email.delete()

            connection.close()
        except Exception as e:
            logger = logging.getLogger('warning_logger')
            logger.error('{}'.format(e.__str__()))

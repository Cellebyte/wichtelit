from __future__ import annotations

import logging
from smtplib import SMTPException, SMTPRecipientsRefused
from typing import List

from django.core import mail
from django.template.loader import render_to_string

from ..models import Status, Wichtelmember

logger = logging.getLogger(__name__)


class Email(object):
    email_template_html = 'mail_template.html'
    email_template_txt = 'mail_template.txt'
    email_subject_prefix = '[Wichtelit] Dein Wichtelpartner für den'

    def senden(self, members: List[Wichtelmember], status=Status.EMAIL_VERSENDET):
        return_values = []
        with mail.get_connection() as connection:
            for member in members:
                if member.status == status:
                    continue
                else:
                    subject = f'{self.email_subject_prefix} {member.wichtelgruppe.wichteldatum}'
                    html_message = render_to_string(
                        self.email_template_html,
                        {
                            'member': member,
                            'current_status': status
                        }
                    )
                    plain_message = render_to_string(
                        self.email_template_txt,
                        {
                            'member': member,
                            'current_status': status
                        }
                    )
                    logger.debug(plain_message)
                    to = f'{member.emailAdresse}'
                    try:
                        email = mail.EmailMultiAlternatives(
                            subject,
                            plain_message,
                            to=[to],
                            connection=connection
                        )
                        email.attach_alternative(
                            html_message,
                            'text/html'
                        )
                        email.send(fail_silently=False)
                        member.status = status
                        member.save()
                    except SMTPRecipientsRefused as e:
                        logger.debug(e)
                        return_values.append(True)
                    except SMTPException as e:
                        logger.debug(e)
                        return_values.append(False)
        return all(return_values)


class EmailGruppeErstellt(Email):
    email_template_html = 'mail_template_created.html'
    email_template_txt = 'mail_template_created.txt'
    email_subject_prefix = '[Wichtelit] Hier dein Link um weitere Leute in deine Gruppe einzuladen'

    def senden(self, member: Wichtelmember, request=None):
        subject = f'{self.email_subject_prefix}'
        html_message = render_to_string(
            self.email_template_html,
            {
                'member': member,
                'request': request
            }
        )
        plain_message = render_to_string(
            self.email_template_txt,
            {
                'member': member,
                'request': request
            }
        )
        logger.debug(plain_message)
        to = f'{member.emailAdresse}'
        with mail.get_connection() as connection:
            try:
                email = mail.EmailMultiAlternatives(
                    subject,
                    plain_message,
                    to=[to],
                    connection=connection
                )
                email.attach_alternative(
                    html_message,
                    'text/html'
                )
                email.send(fail_silently=False)
            except SMTPRecipientsRefused as e:
                logger.debug(e)
                return True
            except SMTPException as e:
                logger.debug(e)
                return False

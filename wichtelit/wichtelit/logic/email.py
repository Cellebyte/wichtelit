from __future__ import annotations

import logging
from smtplib import SMTPException, SMTPRecipientsRefused
from typing import List

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ..models import Status

from ..models import Wichtelmember

logger = logging.getLogger(__name__)


class Email(object):
    email_template = 'mail_template.html'
    email_subject_prefix = '[Wichtelit] Dein Wichtelpartner für den'

    def __init__(self, email: str) -> Email:
        self.email = email

    def senden(self, members: List[Wichtelmember], status=Status.EMAIL_VERSENDET):
        return_values = []
        with mail.get_connection() as connection:
            for member in members:
                if member.status == status:
                    continue
                else:
                    subject = f'{self.email_subject_prefix} {member.wichtelgruppe.wichteldatum}'
                    html_message = render_to_string(
                        self.email_template,
                        {
                            'member': member,
                            'current_status': status,
                            'status': Status
                        }
                    )
                    plain_message = strip_tags(html_message).replace(
                        '&#160;', '')
                    logger.debug(plain_message)
                    from_email = f'WitchtelIt <{self.email}>'
                    to = f'{member.emailAdresse}'
                    try:
                        email = mail.EmailMultiAlternatives(
                            subject,
                            plain_message,
                            from_email,
                            [to],
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

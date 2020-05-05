from __future__ import annotations

import logging
from typing import List

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from smtplib import SMTPException
from ..models import Wichtelmember

logger = logging.getLogger(__name__)


class Email(object):
    email_template = 'mail_template.html'
    email_subject_prefix = '[Wichtelit] Dein Wichtelpartner für den'

    def __init__(self, email: str) -> Email:
        self.email = email

    def senden(self, members: List[Wichtelmember]):
        return_values = []
        for member in members:
            subject = f'{self.email_subject_prefix} {member.wichtelgruppe.wichteldatum}'
            html_message = render_to_string(self.email_template, {'member': member})
            plain_message = strip_tags(html_message).replace('&#160;', '')
            logger.debug(plain_message)
            from_email = f'WitchtelIt <{self.email}>'
            to = f'{member.emailAdresse}'
            try:
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    [to],
                    html_message=html_message,
                    fail_silently=False
                )
                return_values.append(True)
            except SMTPException as e:
                logger.debug(e.__traceback__)
                return_values.append(False)

        return all(return_values)

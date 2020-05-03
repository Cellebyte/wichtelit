from django.core.mail import send_mail
from django.utils.html import strip_tags

from wichtelit.models import Wichtelmember


def emailing(foo):
    for member in Wichtelmember.objects.all():
        send_mail(
            'Erinnernung an das Wichteln.',
            f'Dein Wichtelpartner ist: {member.wichtelmember.wichtelpartner}\n' +
            f'Das Budget liegt bei {member.wichtelmember.wichtelgruppe.budget}\n' +
            f'Am {member.wichtelmember.wichtelgruppe.wichteldatum} wird gewichtelt.\n',
            f'wichtelit@1kbyte.de',
            [f'{member.wichtelmember.emailAdresse}'],
            fail_silently=False,
        )

from wichtelit.models import Wichtelgruppe, Wichtelmember
from django.http import HttpResponse
def emailing(foo):
    for member in Wichtelmember.objects.all():
        send_messages(
            'Erinnernung an das Wichteln.',
            f'Dein Wichtelpartner ist: {member.wichtelmember.wichtelpartner}'+
            f' Das Budget liegt bei {member.wichtelmember.}' +
            f' Am {member.wichtelgruppe.wichteldatum} wird gewichtelt.',
            f'wichtelit@1kbyte.de',
            [f'{member.wichtelmember.emailAdresse}'],
            fail_silently=False,
        )

from datetime import date

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django.forms import DateField, IntegerField, ModelForm, ValidationError

from wichtelit.models import Wichtelgruppe, Wichtelmember


class MemberForm(ModelForm):
    budget = IntegerField(min_value=1, max_value=20)
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def __init__(self, *args, **kwargs):
        self.wichtelgruppe_id = kwargs.pop('wichtelgruppe_id')
        super().__init__(*args, **kwargs)

    def check_emailAdresse(self, emailAdresse):
        if emailAdresse is None:
            raise ValidationError("Bidde eine Email angeben.")
        try:
            _ = Wichtelmember.objects.get(
                wichtelgruppe__id=self.wichtelgruppe_id,
                emailAdresse=emailAdresse
            )
            return False
        except Wichtelmember.DoesNotExist:
            return True

    def clean_emailAdresse(self):
        emailAdresse = self.cleaned_data.get("emailAdresse")
        if not self.check_emailAdresse(emailAdresse):
            raise ValidationError(
                "Tut mir Leid diese Email Adresse wurde in dieser Gruppe schon verwendet."
            )
        return emailAdresse

    class Meta:
        model = Wichtelmember
        exclude = ('wichtelpartner', 'wichtelgruppe', 'id', 'status')


class GruppenForm(ModelForm):
    anmeldeschluss = DateField(input_formats=['%d.%m.%Y'])
    wichteldatum = DateField(input_formats=['%d.%m.%Y'])
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def clean(self):
        cleaned_data = super().clean()
        anmeldeschluss = cleaned_data.get("anmeldeschluss")
        wichteldatum = cleaned_data.get("wichteldatum")
        if anmeldeschluss and wichteldatum:
            if wichteldatum <= anmeldeschluss:
                raise ValidationError(
                    "Das Wichteldatum muss später als der Anmeldeschluss sein."
                )

    def clean_anmeldeschluss(self):
        anmeldeschluss = self.cleaned_data.get('anmeldeschluss')
        if anmeldeschluss < date.today():
            raise ValidationError("Der Anmeldeschluss kann nicht in der Vergangenheit liegen.")
        return anmeldeschluss

    class Meta:
        model = Wichtelgruppe
        exclude = ('id', 'budget', 'status')


__all__ = ['MemberForm', 'GruppenForm']

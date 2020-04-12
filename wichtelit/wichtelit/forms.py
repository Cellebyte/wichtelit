from datetime import date

from django.forms import DateField, IntegerField, ModelForm, ValidationError

from wichtelit.models import Wichtelgruppe, Wichtelmember


class MemberForm(ModelForm):
    budget = IntegerField(min_value=1)

    class Meta:
        model = Wichtelmember
        exclude = ('wichtelpartner', 'wichtelgruppe', 'id')


class GruppenForm(ModelForm):
    ablaufdatum = DateField(input_formats=['%d.%m.%Y'])
    wichteldatum = DateField(input_formats=['%d.%m.%Y'])

    def clean(self):
        cleaned_data = super().clean()
        ablaufdatum = cleaned_data.get("ablaufdatum")
        wichteldatum = cleaned_data.get("wichteldatum")
        if ablaufdatum and wichteldatum:
            if wichteldatum <= ablaufdatum:
                raise ValidationError(
                    "Das Wichteldatum muss später als das Ablaufdatum sein."
                )

    def clean_ablaufdatum(self):
        ablaufdatum = self.cleaned_data.get('ablaufdatum')
        if ablaufdatum < date.today():
            raise ValidationError("Das Ablaufdatum kann nicht in der Vergangenheit liegen.")
        return ablaufdatum

    class Meta:
        model = Wichtelgruppe
        exclude = ('id', 'budget', 'status')


__all__ = ['MemberForm', 'GruppenForm']

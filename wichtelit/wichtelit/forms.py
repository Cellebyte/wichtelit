from django.forms import ModelForm, IntegerField, DateField
from wichtelit.models import Wichtelgruppe, Wichtelmember


class MemberForm(ModelForm):
    budget = IntegerField(min_value=1)

    class Meta:
        model = Wichtelmember
        exclude = ('wichtelpartner', 'wichtelgruppe', 'id')


class GruppenForm(ModelForm):
    ablaufdatum = DateField(input_formats=['%d.%m.%Y'])
    wichteldatum = DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Wichtelgruppe
        exclude = ('id', 'budget')


__all__ = ['MemberForm', 'GruppenForm']

from django.forms import ModelForm, Form, IntegerField, DateField
from wichtelit.models import Wichtelgruppe, Wichtelmember


class MemberForm(ModelForm):
    class Meta:
        model = Wichtelmember
        exclude = ('wichtelpartner', 'wichtelgruppe', 'id')


class GruppenForm(ModelForm):
    ablaufdatum = DateField(input_formats=['%d.%m.%Y'])
    wichteldatum = DateField(input_formats=['%d.%m.%Y'])
    class Meta:
        model = Wichtelgruppe
        exclude = ('id',)


class MemberbudgetForm(Form):
    budget = IntegerField(min_value=0)


__all__ = ['MemberForm', 'GruppenForm', 'MemberbudgetForm']

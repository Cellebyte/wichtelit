import logging
import secrets
from copy import copy
from datetime import date

from django import http
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

from wichtelit.forms import GruppenForm, MemberForm
from wichtelit.models import Status, Wichtelgruppe, Wichtelmember

# Get an instance of a logger
logger = logging.getLogger(__name__)


class MyTemplateView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.name
        return context


class HomeView(MyTemplateView):
    name = 'home'
    template_name = 'home.html'


class ImprintView(MyTemplateView):
    name = 'impressum'
    template_name = 'impressum.html'


class CreatedMemberView(MyTemplateView):
    name = 'created'
    template_name = 'success_MemberForm.html'

    def get(self, request, *args, **kwargs):
        try:
            self.wichtelgruppe = MemberFormView.get_group(
                wichtelgruppe_id=self.kwargs.pop('wichtelgruppe_id')
            )
        except Wichtelgruppe.DoesNotExist:
            return render(request, 'error_NoMemberForm.html')
        kwargs['wichtelgruppe'] = self.wichtelgruppe
        return super().get(request, *args, **kwargs)


class GruppenView(FormView):
    template_name = 'form_GruppenForm.html'
    form_class = GruppenForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.budget = 0
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return str(self.object.id)


class Calculation(View):

    def lostopf(self, members, lostopf):
        for index in range(len(members)):
            not_in_list = False
            loszieher = members[index]
            try:
                lostopf.remove(loszieher.id)
            except ValueError:
                not_in_list = True
            loszieher.wichtelpartner = secrets.choice(
                lostopf
            )
            logger.info(
                f'{loszieher.emailAddress} hat partner {loszieher.wichtelpartner.emailAddress}')
            loszieher.save()
            lostopf.remove(loszieher.wichtelpartner)
            if not not_in_list:
                lostopf.append(loszieher)

    def get(self, request, *args, **kwargs):
        # Nimmt alle Gruppen die erstellt wurden und dessen ablaufdatum kleiner gleich heute ist.
        gruppen = Wichtelgruppe.objects.filter(
            status=Status.ERSTELLT,
            ablaufdatum__lte=date.today()
        )
        for gruppe in gruppen:
            members = Wichtelmember.objects.filter(wichtelgruppe=gruppe)
            lostopf = copy(members)
            if len(members) < 2:
                logger.warning(f'{gruppe.id} hat weniger als 2 member.')
                continue
            else:
                self.lostopf(list(members), list(lostopf))
            gruppe.status = Status.GEWÜRFELT
            gruppe.save()
        return http.HttpResponse("true")


class MemberFormView(FormView):
    template_name = 'form_MemberForm.html'
    form_class = MemberForm

    @staticmethod
    def get_group(wichtelgruppe_id):
        return Wichtelgruppe.objects.get(id=wichtelgruppe_id)

    def check_group_available(self, request):
        try:
            self.wichtelgruppe = MemberFormView.get_group(
                wichtelgruppe_id=self.kwargs.pop('wichtelgruppe_id')
            )
        except Wichtelgruppe.DoesNotExist:
            return render(request, 'error_NoMemberForm.html', status=400)
        if date.today() >= self.wichtelgruppe.ablaufdatum:
            return render(request, 'error_ClosedMemberForm.html', status=403)
        return False

    def get(self, request, *args, **kwargs):
        # Wenn das erste None returned dann wird erst das zweite ausgeführt.
        return self.check_group_available(request) or super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.check_group_available(request) or super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Hier hole ich mir die Wichtelgruppe aus der Datenbank.
        # Hier erstelle ich aus der Eingabemaske das potentielle Objekt.
        self.object = form.save(commit=False)
        # Nun die wichtelgruppe von oben hinzufügen
        self.object.wichtelgruppe = self.wichtelgruppe
        self.wichtelgruppe.budget = self.wichtelgruppe.budget + form.cleaned_data['budget']
        self.object.save()
        self.wichtelgruppe.save()
        return super().form_valid(form)

    def get_success_url(self):
        return f'{str(self.wichtelgruppe.id)}/created'

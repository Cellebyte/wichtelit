from django import http

from wichtelit.forms import GruppenForm, MemberForm
from wichtelit.models import Wichtelgruppe, Wichtelmember
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponse


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


class GruppenView(FormView):
    template_name = 'form_GruppenForm.html'
    form_class = GruppenForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.budget = 0
        self.object.save()
        return super().form_valid(form)
        # return http.HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return str(self.object.id)


# def return_member(foo):
#     members = Wichtelmember.objects.all()
#     content = []
#     for member in members:
#         content.append(f"{member.emailAddress}, {member.budget}")
#     return HttpResponse(content=content, status=200)


class MemberFormView(FormView):
    template_name = 'form_MemberForm.html'
    form_class = MemberForm

    def form_valid(self, form):
        try:
            # Hier hole ich mir die Wichtelgruppe aus der Datenbank.
            wichtelgruppe_id = self.kwargs.pop('wichtelgruppe_id')
            wichtelgruppe = Wichtelgruppe.objects.get(id=wichtelgruppe_id)
            # Hier erstelle ich aus der Eingabemaske das potentielle Objekt.
            self.object = form.save(commit=False)
            # Nun die wichtelgruppe von oben hinzufügen
            self.object.wichtelgruppe = wichtelgruppe
            wichtelgruppe.budget = wichtelgruppe.budget + form.cleaned_data['budget']
            self.object.save()
            wichtelgruppe.save()
            return http.HttpResponse(
                f"Viel Spaß beim wichteln. Am {self.object.wichtelgruppe.wichteldatum} wird gewichtelt."
            )
        except Wichtelgruppe.DoesNotExist:
            return http.HttpResponseNotFound(
                "Die Wichtelgruppe scheint es nicht mehr zu geben."
            )

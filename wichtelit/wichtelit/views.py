import django.http

from wichtelit.forms import GruppenForm

from django.views.generic.edit import FormView


def index(request):
    return django.http.HttpResponse("Hallo Wilkommen zum Wichteln.")


class GruppenView(FormView):
    template_name = 'form_GruppenForm.html'
    form_class = GruppenForm

    def form_valid(self, form):
        self.temp_object = form.save()
        return django.http.HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.temp_object.id

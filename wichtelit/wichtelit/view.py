import django.http


def index(request):
    return django.http.HttpResponse("Hallo Wilkommen zum Wichteln.")

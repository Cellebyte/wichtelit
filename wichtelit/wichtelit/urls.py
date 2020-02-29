"""wichtelit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .logic.email import emailing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('impressum/', views.ImprintView.as_view(), name='impressum'),
    path('wichteln/<uuid:wichtelgruppe_id>', views.MemberView.as_view(), name='member'),
    path('wichteln/', views.GruppenView.as_view(), name='wichteln'),
    path('sendemail', emailing, name="email"),
    # path('wichteln/created/', view.)
]

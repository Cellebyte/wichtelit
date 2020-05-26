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
from django.urls import path

from . import views

urlpatterns = [
    path("robots.txt", views.robots_txt, name="robots.txt"),
    path('members/cleanup', views.Cleanup.as_view(), name='cleanup'),
    path('members/calculate', views.Calculation.as_view(), name='calculate'),
    path('members/sendmail', views.Emailing.as_view(), name="sendmail"),
    path('members/sendlastmail', views.EmailingLastReminder.as_view(), name="sendlastmail"),
    path('', views.HomeView.as_view(), name='home'),
    path('impressum/', views.ImprintView.as_view(), name='impressum'),
    path('datenschutz/', views.DataSafety.as_view(), name='datenschutz'),
    path(
        'wichteln/<uuid:wichtelgruppe_id>',
        views.MemberFormView.as_view(),
        name='memberform'
    ),
    path('wichteln/', views.GruppenView.as_view(), name='wichteln'),
    # path('members', views.return_member, name='members'),
    path(
        'wichteln/<uuid:wichtelgruppe_id>/created',
        views.CreatedMemberView.as_view(),
        name='created'
    )
]

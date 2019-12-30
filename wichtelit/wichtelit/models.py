import uuid
from django.db import models


class Wichtelgruppe(models.Model):
    budget = models.IntegerField()
    ablaufdatum = models.DateField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Wichtelmember(models.Model):
    vorname = models.CharField(max_length=20)
    nachname = models.CharField(max_length=20)
    emailAdress = models.EmailField(max_length=40)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wichtelgruppe = models.ForeignKey(Wichtelgruppe, on_delete=models.CASCADE)
    wichtelpartner = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

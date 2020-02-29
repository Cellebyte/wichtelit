import uuid
from django.db import models


class Wichtelgruppe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget = models.IntegerField(null=True, blank=True)
    ablaufdatum = models.DateField()
    wichteldatum = models.DateField()


class Wichtelmember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vorname = models.CharField(max_length=20)
    nachname = models.CharField(max_length=20)
    emailAddress = models.EmailField(max_length=40)
    wichtelgruppe = models.ForeignKey(Wichtelgruppe, on_delete=models.CASCADE)
    wichtelpartner = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def budget(self) -> int:
        return self.wichtelgruppe.budget / len(
            Wichtelmember.objects.filter(
                wichtelgruppe=self.wichtelgruppe
            )
        )

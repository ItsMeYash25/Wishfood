from django.db import models

class TableReserve(models.Model):
    username = models.CharField(max_length=120, null=True, blank=True)
    date = models.CharField(max_length=120, blank=True, null=True)
    time = models.CharField(max_length=120, blank=True, null=True)
    member = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.username
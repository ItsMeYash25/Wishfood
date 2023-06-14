from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name
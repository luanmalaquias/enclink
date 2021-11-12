from django.db import models

# Create your models here.

class Url(models.Model):
    data = models.DateField(auto_now=True)
    urlOriginal = models.CharField(primary_key=True, max_length=500, null=False, blank=False)
    urlEncurtada = models.CharField(unique=True, max_length=500, null=False, blank=False)
    usuario = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.urlEncurtada)

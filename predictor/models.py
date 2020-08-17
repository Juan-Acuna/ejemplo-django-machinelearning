from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Atributo(models.Model):
    v_acidity = models.FloatField()
    r_sugar   = models.FloatField()
    alcohol   = models.FloatField()

    def __str__(self):
        return '{} {} {}'.format(str(self.v_acidity), str(self.r_sugar), str(self.alcohol))

class Calidad(models.Model):
    quality = models.FloatField()

    def __str__(self):
        return '{}'.format(str(self.quality))

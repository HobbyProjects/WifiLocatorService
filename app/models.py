from __future__ import unicode_literals

from django.db import models

# Create your models here.
class WifiPoint(models.Model):
    wifiName     = models.CharField(max_length=200)
    password     = models.CharField(max_length=200)
    loc_lat      = models.DecimalField(max_digits=8, decimal_places=6)
    loc_long     = models.DecimalField(max_digits=9, decimal_places=6)
    dest_to_orig = models.DecimalField(max_digits=15,decimal_places=6)

    def __str__(self):
        return self.wifiName

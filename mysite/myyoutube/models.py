from django.db import models
from datetime import datetime


class AllFileUrl(models.Model):
    url = models.CharField(max_length=200)
    uploaded = models.DateTimeField()
    name = models.CharField(max_length=200)
    rate = models.FloatField(max_length=200)
    rate_num = models.IntegerField(max_length=200)

class AllVidFileUrl(models.Model):
    url = models.CharField(max_length=200)
    uploaded = models.DateTimeField()
    name = models.CharField(max_length=200)
    rate = models.FloatField(max_length=200)
    rate_num = models.IntegerField(max_length=200)


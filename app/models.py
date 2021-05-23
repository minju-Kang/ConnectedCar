# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserSettings(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    color = models.IntegerField(default=0)
    wNews = models.IntegerField(default=0)
    wStock = models.IntegerField(default=0)
    wWeather = models.IntegerField(default=0)
    wMail = models.IntegerField(default=0)
    wCalander = models.IntegerField(default=0)
    mail = models.CharField(max_length=50)

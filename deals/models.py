from django.db import models


# Create your models here.
class Deal(models.Model):
    person_id = models.IntegerField()
    ticker = models.CharField(max_length=20)
    adj = models.FloatField()
    volume = models.IntegerField()

from django.db import models
from django.contrib.auth import User

# Create your models here.


class Vehicle(models):
    gama = models.IntegerField(default=0)
    placa = models.CharField()
    style = models.CharField()


class Reserva(models.Model):
    starttime = models.DateField()
    endtime = models.DateField()
    actualtime = models.DateField()
    renter = models.ForeignKey(User)
    vehicle = models.ForeignKey(Vehicle)
    isAccepted = models.BooleanField(default=False)

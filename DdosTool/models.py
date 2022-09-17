from django.db import models


# Create your models here.
class Devices(models.Model):
    ip = models.TextField(unique=True, max_length=15)
    username = models.TextField(default=None)
    password = models.TextField(default=None)


class Commands(models.Model):
    title = models.TextField()
    commandText = models.TextField()
    bandwidth = models.DecimalField(default=0, max_digits=5, decimal_places=1)


class KeyPairs(models.Model):
    title = models.TextField()
    fileName = models.TextField()

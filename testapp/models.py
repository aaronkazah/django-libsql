from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    established_date = models.DateField()

    def __str__(self):
        return self.name

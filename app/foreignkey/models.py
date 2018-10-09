from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

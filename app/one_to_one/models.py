from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.name} the place'


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.place.name} the restaurant'


class Waiter(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{name} the waiter at {restaurant}'.format(
            name=self.name,
            restaurant=self.restaurant,
        )

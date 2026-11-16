from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=[(s, s) for s in
        ['Sedan', 'SUV', 'Wagon', 'Hatchback', 'Coupe', 'Convertible', 'Minivan']])
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2026)])

    class Meta:
        unique_together = ('car_make', 'name', 'year')

    def __str__(self):
        return f'{self.car_make} {self.name} ({self.year})'

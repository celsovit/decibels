from django.db import models
from django.urls import reverse

from location.models import Location

class Measurement(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name='Localização')
    registration_date = models.DateTimeField(verbose_name='Data Registro')
    measured_value = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Valor Medido')

    def __str__(self):
        return f'Location: {self.location}, Date: {self.registration_date}, Value: {self.measured_value}'

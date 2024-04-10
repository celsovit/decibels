from django.db import models

from organization.models import Organization

class Location(models.Model):
    
    name = models.CharField(max_length=60, verbose_name='Nome', help_text='Nome da Locação')
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name='Unidade Organização')
    threshold = models.IntegerField(default=50, verbose_name='Limite', help_text='Limite Aceitável')

    def __str__(self):
        return self.name

from django.db import models
from django.urls import reverse

class Organization(models.Model):
    
    name = models.CharField(max_length=60, verbose_name='Nome', help_text='Nome da organização')
    image_file = models.ImageField(upload_to='brasoes/', verbose_name='Arquivo de imagem')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name
from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    lat  = models.DecimalField(max_digits=9, decimal_places=6)   # e.g., 33.7490
    lng  = models.DecimalField(max_digits=9, decimal_places=6)   # e.g., -84.3880

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

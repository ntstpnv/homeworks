from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=32, unique=True)
    release_date = models.DateField()
    price = models.PositiveIntegerField()
    image = models.URLField(max_length=128, unique=True)
    lte_exists = models.BooleanField()

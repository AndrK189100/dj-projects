from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    image = models.URLField()
    release_date = models.CharField(max_length=10)
    lte_exists = models.BooleanField()
    slug = models.SlugField()



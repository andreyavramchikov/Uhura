from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()

    def __unicode__(self):
        return self.name


class ProductAudio(models.Model):
    product = models.ForeignKey(Product)
    url = models.CharField(max_length=235)


class ProductPDF(models.Model):
    product = models.ForeignKey(Product)
    url = models.CharField(max_length=235)


class ProductPaperback(models.Model):
    product = models.ForeignKey(Product)
    url = models.CharField(max_length=235)
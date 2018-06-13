from django.db import models

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

class Product(models.Model):
    product = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    position = models.IntegerField()
    url = models.CharField(max_length=100)

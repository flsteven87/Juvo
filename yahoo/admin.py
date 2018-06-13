from django.contrib import admin

# Register your models here.

from .models import Category

admin.site.register(Category)

from .models import Product

admin.site.register(Product)

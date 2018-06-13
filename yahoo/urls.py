from django.urls import path

from . import views

urlpatterns = [
    path('', views.interface, name='interface'),
    path('query', views.query, name='query'),
]

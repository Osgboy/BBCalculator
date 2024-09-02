from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('apple-touch-icon.png', RedirectView.as_view(url='/static/apple-touch-icon.png', permanent=True))
]

from django.urls import path
from rest_framework import routers

from animals.views import AnimalView

urlpatterns = [
   path('', AnimalView.as_view()),
]
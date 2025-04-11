from django.urls import path
from .views import get_numbers

urlpatterns=[
    path('numbers/<str:numberid>/',get_numbers),
]
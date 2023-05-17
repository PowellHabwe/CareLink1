from django.urls import path
from . import views

urlpatterns = [
    path('nearest_hospitals/', views.get_nearest_hospitals, name='nearest_hospitals'),
]


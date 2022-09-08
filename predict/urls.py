from django.urls import path
from . import views

app_name='predict'

urlpatterns = [
    path('', views.indexView, name = 'indexView'),

    path('predictfile/', views.predictfile, name='predictfile'),
]
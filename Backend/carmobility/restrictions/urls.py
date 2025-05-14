from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('check_restrictions/', views.check_restrictions, name='check_restrictions'),
]

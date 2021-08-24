from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'), 
    path('method/<int:pk>/', views.cipher, name='method'),] 
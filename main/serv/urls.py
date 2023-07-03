from django.urls import path
from . import views


urlpatterns = [
    path('', views.serv, name='serv'),
    path('<slug:slug>/', views.serv_detail, name='serv_detail'),
  
]
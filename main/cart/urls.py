from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('get/', views.cart_get, name='cart_get'),
    
    path('add/<product_id>/', views.cart_add, name='cart_add'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),
    path('minus/<product_id>/', views.cart_minus, name='cart_minus'),
    path('plus/<product_id>/', views.cart_plus, name='cart_plus'),
    path('add_zakaz/', views.add_zakaz, name='add_zakaz'),
    path('remove_zakaz/', views.remove_zakaz, name='remove_zakaz'),
    path('plus_zakaz/', views.plus_zakaz, name='plus_zakaz'),
    path('minus_zakaz/', views.minus_zakaz, name='minus_zakaz'),
]
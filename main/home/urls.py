
from django.urls import path


from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('vin/', views.vin, name='vin'),
    path('search/', views.search, name='search_results'),
    path('gallery/', views.gallery, name='gallery'),
    path('search_rossko/', views.search_rossko, name='search_rossko'),
    path('search_shate_m/', views.search_shate_m, name='search_shate_m'),
    path('search_favorit/', views.search_favorit, name='search_favorit'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),


    path("robots.txt", views.robots_txt),
]


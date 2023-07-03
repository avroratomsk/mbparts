

from django.urls import re_path, path
from . import views

app_name = "account"
urlpatterns = [
    path("login/", views.login, name="account_login"),


    path("my_login/", views.my_login, name="my_login"),
    path("signup/", views.my_signup, name="account_signup"),
    path('logout/', views.my_logout, name='my_logout'),

    re_path(r'^profile/$', views.profile, name='account_profile'),
    re_path(r'^profile/password/$', views.account_password, name='account_password'),
    re_path(r'^profile/password/update/$', views.password_update, name='password_update'),
    re_path(r'^profile/password/reset/$', views.account_password_reset, name='account_password_reset'),
    re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
    re_path(r'^profile/orders/$', views.profile_orders, name='profile_orders'),
    re_path(r'^profile/wishlist/$', views.profile_wishlist, name='profile_wishlist'),
    re_path(r'^profile/history/$', views.profile_history, name='profile_history'),
   


]
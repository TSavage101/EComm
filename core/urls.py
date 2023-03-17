from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.authe, name='auth'),
    path('logout/', views.logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('product/', views.home, name='product'),
    path('productdetails', views.home, name='productd'),
]

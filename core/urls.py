from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.authe, name='auth'),
    path('logout/', views.logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('products/page<int:pn>', views.products, name='products'),
    path('products/<str:type>/<int:pn>', views.productsa, name='productsa'),
    path('productdetails/<int:pk>', views.productdetails, name='productdetails'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('remove/', views.remove, name='remove'),
    path('comments/<str:prodid>', views.comments, name='commnets'),
    path('products/search_<str:search>/<str:type>', views.productsearch, name='productsearch'),
]

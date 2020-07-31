from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns= [
    path('', views.dashboard, name='dashboard'),
    path('seller/products', views.seller_products, name='seller_products'),
    path('seller/create_product', views.create_product, name='create_product'),
    path('seller/edit_product/<str:product_id>', views.edit_product, name='edit_product'),
    path('seller/delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    path('seller/baskets', views.seller_baskets, name='seller_baskets'),
    path('seller/create_basket', views.create_basket, name='create_basket'),
    path('seller/edit_basket/<str:basket_id>', views.edit_basket, name='edit_basket'),
    path('seller/delete_basket/<str:basket_id>', views.delete_basket, name='delete_basket'),
    path('seller/customers', views.seller_customers, name='seller_customers'),
    path('seller/create_customers', views.create_customers, name='create_customers'),
    path('seller/edit_customer/<str:pk>', views.edit_customer, name='edit_customer'),
    path('seller/delete_customer/<str:pk>', views.delete_customer, name='delete_customer'),
    path('seller/locations',views.seller_locations,name='seller_locations'),
    path('seller/create_locations',views.create_locations,name='create_locations'),
    path('seller/edit_locations/<str:pk>',views.edit_location,name='edit_location' ),
    path('seller/delete_location/<str:pk>',views.delete_location,name='delete_location'),
    path('seller/register',views.register_seller,name='register_seller'),
    path('seller/create_seller',views.create_seller, name='create_seller')
]
from django.urls import path

from .view.user import user_views
from .view.customer import customer_views
from .view.product import product_views
from .view.payment import payment_views

urlpatterns = [
    path('login', user_views.user_login, name='user_login'),
    path('users_all', user_views.user_list, name='user_list'),
    path('users/create', user_views.user_create, name='user_create'),
    path('users/<int:pk>/', user_views.user_detail, name='user_detail'),
    path('users/<int:pk>/update/', user_views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', user_views.user_delete, name='user_delete'),

    path('customers/', customer_views.customer_list, name='customer_list'),
    path('customers/create/', customer_views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', customer_views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/update/', customer_views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', customer_views.customer_delete, name='customer_delete'),

    path('products', product_views.product_list, name='product_list'),
    path('products/licores', product_views.product_list_liquars, name='product_list'),
    path('products/cervezas', product_views.product_list_beer, name='product_list'),
    path('products/otros', product_views.product_list_otros, name='product_list'),
    path('products/golosinas', product_views.product_list_candy, name='product_list'),
    path('products/create', product_views.product_create, name='product_create'),
    path('products/<int:pk>/', product_views.product_detail, name='product_detail'),
    path('products/<int:pk>/update/', product_views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', product_views.product_delete, name='product_delete'),
    path('products/random/<str:category>', product_views.product_random_by_category, name='product_random_by_category'),

    path('payments/', payment_views.payment_list, name='payment_list'),
    path('payments/create/', payment_views.payment_create, name='payment_create'),
    path('payments/<int:pk>/', payment_views.payment_detail, name='payment_detail'),
    path('payments/<int:pk>/update/', payment_views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', payment_views.payment_delete, name='payment_delete'),
]
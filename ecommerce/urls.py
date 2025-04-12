# ecommerce/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.product_list, name='product_list'),
    path('<int:product_id>/', views.single_product, name='single_product'),
]

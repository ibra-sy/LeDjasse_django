from django.urls import path
from .views import ProduitListAPIView, ArticleListAPIView

urlpatterns = [
    path('produits/', ProduitListAPIView.as_view(), name='api-produits'),
    path('articles/', ArticleListAPIView.as_view(), name='api-articles'),
]

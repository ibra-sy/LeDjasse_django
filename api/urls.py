from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProduitViewSet, ArticleViewSet

router = DefaultRouter()
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
]

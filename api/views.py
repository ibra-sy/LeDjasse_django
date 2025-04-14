from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ecommerce.models import Produit
from blog.models import Article
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import ProduitSerializer, ArticleSerializer  # ✅ Import direct

class ProduitListAPIView(generics.ListAPIView):
    queryset = Produit.objects.filter(en_ligne=True)
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categorie', 'etat']


class ArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(statut='publié')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

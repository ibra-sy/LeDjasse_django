from rest_framework import viewsets
from ecommerce.models import Produit
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProductSerializer

from rest_framework import serializers
from ecommerce.models import Produit

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

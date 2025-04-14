from rest_framework import serializers
from ecommerce.models import Produit
from blog.models import Article

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'titre', 'prix']  # ✨ liste explicite et sûre

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'titre', 'contenu', 'categorie', 'image', 'auteur', 'statut', 'date_publication']  # ⚠️ NE MET PAS extrait s'il n'existe pas

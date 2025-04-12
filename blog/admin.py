from django.contrib import admin
from .models import Categorie, Tag, Article, Commentaire

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['nom']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_publication', 'statut', 'categorie')
    list_filter = ('statut', 'categorie', 'tags')
    search_fields = ('titre', 'contenu')
    date_hierarchy = 'date_publication'
    filter_horizontal = ()
    autocomplete_fields = ['tags']

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('article', 'utilisateur', 'date')
    list_filter = ('date',)

from django.contrib import admin
from .models import Categorie, Tag, Article, Commentaire
from ecommerce.models import ProfilUtilisateur
from tinymce.widgets import TinyMCE
from django.db import models



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
    autocomplete_fields = ['tags']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
        }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "auteur":
            vendeurs_ids = ProfilUtilisateur.objects.filter(role='vendeur').values_list('user_id', flat=True)
            kwargs["queryset"] = self.model._meta.get_field("auteur").related_model.objects.filter(id__in=vendeurs_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('article', 'utilisateur', 'date')
    list_filter = ('date',)

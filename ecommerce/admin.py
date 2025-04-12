from django.contrib import admin
from .models import Categorie, Produit, Commande, Conversation, Message

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('titre', 'vendeur', 'prix', 'etat', 'statut', 'en_ligne')
    list_filter = ('statut', 'etat', 'en_ligne', 'categorie')
    search_fields = ('titre', 'description')

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'produit', 'acheteur', 'date_commande', 'statut')
    list_filter = ('statut',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('participant1', 'participant2', 'created_at')
    search_fields = ('participant1__username', 'participant2__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'expediteur', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('expediteur__username', 'contenu')

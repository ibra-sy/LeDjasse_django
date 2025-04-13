from django.contrib import admin
from .models import Categorie, Produit, Commande, Conversation, Message, ProfilUtilisateur
from django.contrib.auth import get_user_model

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)

User = get_user_model()

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('titre', 'vendeur', 'prix', 'etat', 'statut', 'en_ligne')
    list_filter = ('statut', 'etat', 'en_ligne', 'categorie')
    search_fields = ('titre', 'description')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "vendeur":
            # ✅ correction ici : user_id et non utilisateur_id
            vendeurs_ids = ProfilUtilisateur.objects.filter(role='vendeur').values_list('user_id', flat=True)
            kwargs["queryset"] = User.objects.filter(id__in=vendeurs_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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



@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
# ecommerce/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.product_list, name='product_list'),
    path('<int:product_id>/', views.single_product, name='single_product'),
    path('ajouter-produit/', views.ajouter_produit, name='ajouter_produit'),
    path('devenir-vendeur/', views.devenir_vendeur, name='devenir_vendeur'),
    path('messages/', views.messagerie_accueil, name='messagerie_accueil'),
    path('messages/conversation/<int:conversation_id>/', views.afficher_conversation, name='afficher_conversation'),
    path('messages/demarrer/<int:user_id>/', views.demarrer_conversation, name='demarrer_conversation'),
    path('confirmer-achat/<int:produit_id>/', views.confirmer_achat, name='confirmer_achat'),
    path('mes-achats/', views.mes_achats, name='mes_achats'),
    path('confirmer-vente/', views.confirmer_vente, name='confirmer_vente'),
    
]

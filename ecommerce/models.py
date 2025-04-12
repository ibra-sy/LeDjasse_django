from django.db import models
from django.conf import settings
from django.utils import timezone

# Partie E-commerce
class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom

class Produit(models.Model):
    STATUTS = [
        ('disponible', 'Disponible'),
        ('vendu', 'Vendu'),
    ]
    ETATS = [
        ('neuf', 'Neuf'),
        ('occasion', 'Occasion'),
        ('tres_bon', 'Très bon état'),
        ('bon', 'Bon état'),
        ('acceptable', 'Acceptable'),
    ]
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    prix = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix")
    en_ligne = models.BooleanField(default=True, verbose_name="En ligne")
    statut = models.CharField(max_length=20, choices=STATUTS, default='disponible', verbose_name="Statut")
    etat = models.CharField(max_length=20, choices=ETATS, default='occasion', verbose_name="État")
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Vendeur")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, verbose_name="Catégorie")
    image = models.ImageField(upload_to='produits/', null=True, blank=True, verbose_name="Image du produit")

    def __str__(self):
        return self.titre

class Commande(models.Model):
    STATUTS_COMMANDE = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
    ]
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    acheteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Acheteur")
    date_commande = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")
    statut = models.CharField(max_length=20, choices=STATUTS_COMMANDE, default='en_attente', verbose_name="Statut")

    def __str__(self):
        return f"Commande {self.id} - {self.produit.titre}"

# Partie Messagerie intégrée
class Conversation(models.Model):
    participant1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='conversations_initiees', 
        on_delete=models.CASCADE,
        verbose_name="Participant 1"
    )
    participant2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='conversations_receptionnees', 
        on_delete=models.CASCADE,
        verbose_name="Participant 2"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        unique_together = ('participant1', 'participant2')
        ordering = ['-created_at']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        return f"Conversation entre {self.participant1.username} et {self.participant2.username}"

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, 
        related_name='messages', 
        on_delete=models.CASCADE,
        verbose_name="Conversation"
    )
    expediteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='messages_envoyes', 
        on_delete=models.CASCADE,
        verbose_name="Expéditeur"
    )
    contenu = models.TextField(verbose_name="Contenu du message")
    date_envoi = models.DateTimeField(default=timezone.now, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        ordering = ['date_envoi']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message de {self.expediteur.username} le {self.date_envoi.strftime('%d/%m/%Y %H:%M')}"

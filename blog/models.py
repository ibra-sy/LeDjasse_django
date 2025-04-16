from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom

class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True, verbose_name="Nom du tag")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.nom

class Article(models.Model):
    CHOIX_STATUT = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]
    titre = models.CharField(max_length=200, verbose_name="Titre")
    contenu = HTMLField(verbose_name="Contenu")
    image = models.ImageField(upload_to='blog/', null=True, blank=True, verbose_name="Image de l'article")
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    statut = models.CharField(max_length=10, choices=CHOIX_STATUT, default='brouillon', verbose_name="Statut")
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Auteur")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, verbose_name="Catégorie")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires', verbose_name="Article")
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    contenu = models.TextField(verbose_name="Contenu")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date du commentaire")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reponses')

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['date']

    def __str__(self):
        return f"Commentaire de {self.utilisateur.username} sur {self.article.titre}"
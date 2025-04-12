from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Article, Commentaire

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'tags': FilteredSelectMultiple("Tags", is_stacked=False),
        }

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Écrire un commentaire...'
            })
        }
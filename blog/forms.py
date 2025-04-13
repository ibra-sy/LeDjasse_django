from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Article, Commentaire
from tinymce.widgets import TinyMCE


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

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image', 'categorie', 'tags']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': TinyMCE(attrs={'cols': 80, 'rows': 15}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
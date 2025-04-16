from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Article, Commentaire, Tag, Categorie
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
    categorie = forms.CharField(
        label="Catégorie",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'categorie-options'})
    )

    tags = forms.CharField(
        label="Tags (séparés par des virgules)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : voyage, sport'})
    )

    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image', 'categorie', 'tags']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': TinyMCE(attrs={'cols': 80, 'rows': 15}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_categorie(self):
        nom = self.cleaned_data['categorie'].strip()
        obj, _ = Categorie.objects.get_or_create(nom=nom)
        return obj

    def clean_tags(self):
        noms = [t.strip() for t in self.cleaned_data['tags'].split(',') if t.strip()]
        return [Tag.objects.get_or_create(nom=nom)[0] for nom in noms]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.categorie = self.cleaned_data['categorie']
        if commit:
            instance.save()
            instance.tags.set(self.cleaned_data['tags'])
        return instance
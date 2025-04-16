from django import forms
from .models import Achat, Produit, ProfilUtilisateur, Categorie
from django.contrib.auth import get_user_model

User = get_user_model()

class ProduitForm(forms.ModelForm):
    categorie = forms.CharField(
        label="Catégorie",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Produit
        fields = ['titre', 'description', 'prix', 'etat', 'categorie', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l’article'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix en Franc CFA'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # ✅ Empêche la saisie si l'utilisateur n'est pas vendeur
        if user:
            try:
                if user.profilutilisateur.role != 'vendeur':
                    for field in self.fields:
                        self.fields[field].disabled = True
            except ProfilUtilisateur.DoesNotExist:
                for field in self.fields:
                    self.fields[field].disabled = True

        # ✅ Préparer une liste pour datalist dans le template
        self.existing_categories = Categorie.objects.all()

    def clean_categorie(self):
        data = self.cleaned_data.get('categorie')

        if not data:
            raise forms.ValidationError("Veuillez entrer ou sélectionner une catégorie.")

        # ✅ Cherche une catégorie existante par nom (insensible à la casse)
        categorie = Categorie.objects.filter(nom__iexact=data.strip()).first()

        if not categorie:
            # ✅ Crée la nouvelle catégorie
            categorie = Categorie.objects.create(nom=data.strip())

        return categorie

class ConfirmationAchatForm(forms.Form):
    ville = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    commune = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    quartier = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rue = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['ville', 'commune', 'quartier', 'rue', 'email']
        widgets = {
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'commune': forms.TextInput(attrs={'class': 'form-control'}),
            'quartier': forms.TextInput(attrs={'class': 'form-control'}),
            'rue': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
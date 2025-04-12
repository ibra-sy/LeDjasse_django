from django.shortcuts import render, get_object_or_404
from .models import Produit, Categorie

def product_list(request):
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        produits = Produit.objects.filter(en_ligne=True, statut='disponible', categorie__id=categorie_id)
    else:
        produits = Produit.objects.filter(en_ligne=True, statut='disponible')
    
    categories = Categorie.objects.all()
    return render(request, 'ecommerce/product_list.html', {'produits': produits, 'categories': categories})

def single_product(request, product_id):
    # Récupère le produit dont l'id est passé en paramètre
    produit = get_object_or_404(Produit, id=product_id)
    return render(request, 'ecommerce/single-product.html', {'produit': produit})

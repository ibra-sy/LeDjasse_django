from django.shortcuts import redirect, render, get_object_or_404
from .models import Achat, Conversation, Produit, Categorie, Message
from django.contrib.auth.decorators import login_required
from .forms import ConfirmationAchatForm, ProduitForm
from .models import Produit, ProfilUtilisateur
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode


from django.contrib.auth import get_user_model
User = get_user_model()

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

@login_required
def ajouter_produit(request):
    if not hasattr(request.user, 'profilutilisateur') or request.user.profilutilisateur.role != 'vendeur':
        messages.error(request, "Seuls les vendeurs peuvent ajouter des produits.")
        return redirect('product_list')

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.vendeur = request.user
            produit.save()
            messages.success(request, "Votre article a été ajouté avec succès.")
            return redirect('product_list')
    else:
        form = ProduitForm(user=request.user)

    return render(request, 'ecommerce/ajouter_produit.html', {'form': form})

@login_required
def devenir_vendeur(request):
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # ✅ Mettre à jour l'email de l'utilisateur connecté
            if request.user.email != email:
                request.user.email = email
                request.user.save()

            message = "Votre demande a été enregistrée. Vous recevrez un e-mail une fois la validation effectuée par l'admin."

            # ✅ Envoi d'un e-mail de confirmation au candidat
            send_mail(
                subject="Demande pour devenir vendeur",
                message="Bonjour,\n\nNous avons bien reçu votre demande pour devenir vendeur sur LeDjassa. Un administrateur la traitera dans les plus brefs délais.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

    return render(request, 'pages/devenir_vendeur.html', {'message': message})

@login_required
def messagerie_accueil(request):
    conversations = Conversation.objects.filter(
        participant1=request.user
    ) | Conversation.objects.filter(
        participant2=request.user
    )
    return render(request, 'ecommerce/messagerie_accueil.html', {'conversations': conversations})

@login_required
def afficher_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.participant1 and request.user != conversation.participant2:
        return redirect('messagerie_accueil')

    messages = conversation.messages.all()

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            Message.objects.create(conversation=conversation, expediteur=request.user, contenu=contenu)
            return redirect('afficher_conversation', conversation_id=conversation.id)

    return render(request, 'ecommerce/afficher_conversation.html', {'conversation': conversation, 'messages': messages})

@login_required
def demarrer_conversation(request, user_id):
    autre_user = get_object_or_404(User, id=user_id)

    # Rechercher une conversation existante dans les deux sens
    conversation = Conversation.objects.filter(
        participant1=request.user, participant2=autre_user
    ).first() or Conversation.objects.filter(
        participant1=autre_user, participant2=request.user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(
            participant1=request.user, participant2=autre_user
        )

    return redirect('afficher_conversation', conversation_id=conversation.id)



@login_required
def confirmer_achat(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        form = ConfirmationAchatForm(request.POST)
        if form.is_valid():
            email_client = form.cleaned_data['email']
            ville = form.cleaned_data['ville']
            commune = form.cleaned_data['commune']
            quartier = form.cleaned_data['quartier']
            rue = form.cleaned_data['rue']

            # Envoie du mail au client
            send_mail(
                subject='Confirmation de votre commande',
                message=f"Merci pour votre achat de l'article '{produit.titre}'.\n\n"
                        f"Adresse de livraison : {rue}, {quartier}, {commune}, {ville}\n\n"
                        f"Prix : {produit.prix} Franc CFA",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_client],
                fail_silently=False,
            )

            # Génère le lien de confirmation pour le vendeur
            query_params = urlencode({
                'produit_id': produit.id,
                'email_client': email_client,
                'ville': ville,
                'commune': commune,
                'quartier': quartier,
                'rue': rue,
            })
            confirmation_url = request.build_absolute_uri(reverse('confirmer_vente') + f"?{query_params}")

            # ✅ Envoie du mail au vendeur
            if produit.vendeur.email:
                send_mail(
                    subject="Nouvelle commande à confirmer",
                    message=f"Votre produit '{produit.titre}' vient d'être commandé.\n\n"
                            f"Un client a indiqué vouloir l'acheter. Cliquez sur le lien ci-dessous pour confirmer la vente :\n\n"
                            f"{confirmation_url}\n\n"
                            f"Merci d'utiliser LeDjassa.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[produit.vendeur.email],
                    fail_silently=False,
                )
            else:
                print("⚠️ Aucun e-mail trouvé pour le vendeur :", produit.vendeur.username)

            messages.success(request, "Confirmation envoyée avec succès !")
            return redirect('product_list')
    else:
        form = ConfirmationAchatForm(initial={'email': request.user.email})

    return render(request, 'ecommerce/confirmer_achat.html', {'produit': produit, 'form': form})

@login_required
def confirmer_vente(request):
    produit_id = request.GET.get('produit_id')
    produit = get_object_or_404(Produit, id=produit_id)

    # Vérifie que seul le vendeur peut confirmer
    if produit.vendeur != request.user:
        messages.error(request, "Accès interdit.")
        return redirect('product_list')

    if request.method == 'POST':
        produit.delete()
        messages.success(request, "La vente a été confirmée. Le produit a été retiré.")
        return redirect('product_list')

    context = {
        'produit': produit,
        'email_client': request.GET.get('email_client'),
        'ville': request.GET.get('ville'),
        'commune': request.GET.get('commune'),
        'quartier': request.GET.get('quartier'),
        'rue': request.GET.get('rue'),
    }
    return render(request, 'ecommerce/confirmer_vente.html', context)

@login_required
def mes_achats(request):
    achats = Achat.objects.filter(utilisateur=request.user)
    return render(request, 'ecommerce/mes_achats.html', {'achats': achats})
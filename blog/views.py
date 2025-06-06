from django.shortcuts import redirect, render, get_object_or_404

from ecommerce.models import ProfilUtilisateur
from .models import Article, Commentaire, Categorie, Tag
from .forms import ArticleForm, CommentaireForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.paginator import Paginator


def blog_list(request):
    categorie_id = request.GET.get('categorie')
    paginated = False

    if categorie_id:
        # Si une catégorie est sélectionnée, pas de pagination
        articles = Article.objects.filter(statut='publie', categorie__id=categorie_id).order_by('-date_publication')
    else:
        # Sinon, on applique la pagination
        all_articles = Article.objects.filter(statut='publie').order_by('-date_publication')
        paginator = Paginator(all_articles, 4)  # 6 articles par page
        page = request.GET.get('page')
        articles = paginator.get_page(page)
        paginated = True

    blog_categories = Categorie.objects.all()

    return render(request, 'blog/blog.html', {
        'articles': articles,
        'blog_categories': blog_categories,
        'paginated': paginated
    })

@login_required
def single_blog(request, pk):
    article = get_object_or_404(Article, pk=pk)
    commentaires = article.commentaires.filter(parent__isnull=True)
    previous_article = Article.objects.filter(id__lt=article.id).order_by('-id').first()
    next_article = Article.objects.filter(id__gt=article.id).order_by('id').first()
    recent_posts = Article.objects.exclude(id=pk).order_by('-date_publication')[:3]

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        parent_id = request.POST.get('parent_id')
        modifier_id = request.POST.get('modifier_id')
        supprimer_id = request.POST.get('supprimer_id')

        # ✅ Suppression
        if supprimer_id and request.user.is_authenticated:
            commentaire = get_object_or_404(Commentaire, id=supprimer_id, utilisateur=request.user)
            commentaire.delete()
            return redirect('single_blog', pk=pk)

        # ✅ Modification
        if modifier_id and request.user.is_authenticated:
            commentaire = get_object_or_404(Commentaire, id=modifier_id, utilisateur=request.user)
            if contenu:  # ✅ On vérifie que le contenu n'est pas vide
                commentaire.contenu = contenu
                commentaire.save()
                return redirect('single_blog', pk=pk)
            else:
                messages.error(request, "Le contenu ne peut pas être vide.")

        # ✅ Nouveau commentaire ou réponse
        if contenu and request.user.is_authenticated:
            commentaire = Commentaire(article=article, utilisateur=request.user, contenu=contenu)
            if parent_id:
                parent = get_object_or_404(Commentaire, id=parent_id)
                commentaire.parent = parent
            commentaire.save()
            return redirect('single_blog', pk=pk)

    return render(request, 'blog/single-blog.html', {
        'article': article,
        'previous_article': previous_article,
        'next_article': next_article,
        'recent_posts': recent_posts,
        'commentaires': commentaires,
    })


def blog_by_tag(request, slug):
    tag = get_object_or_404(Tag, nom=slug)
    articles = Article.objects.filter(tags=tag, statut='publie')
    return render(request, 'blog/blog.html', {'articles': articles, 'selected_tag': tag})


@login_required
def ajouter_article_blog(request):
    try:
        profil = request.user.profilutilisateur
        if profil.role != 'vendeur':
            return redirect('blog')  # redirige les non-vendeurs

        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                article = form.save(commit=False)
                article.auteur = request.user
                article.save()
                form.save_m2m()
                return redirect('blog')
        else:
            form = ArticleForm()
        return render(request, 'blog/ajouter_article.html', {'form': form})

    except ProfilUtilisateur.DoesNotExist:
        return redirect('blog')

@login_required
def modifier_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if article.auteur != request.user:
        messages.error(request, "Vous n’avez pas la permission de modifier cet article.")
        return redirect('blog')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article modifié avec succès.")
            return redirect('single_blog', pk=article.pk)
    else:
        initial = {
            'categorie': article.categorie.nom if article.categorie else '',
            'tags': ", ".join(tag.nom for tag in article.tags.all()),
        }
        form = ArticleForm(instance=article, initial=initial)

    return render(request, 'blog/modifier_article.html', {
        'form': form,
        'article': article,
    })

@login_required
def supprimer_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, auteur=request.user)

    if request.method == 'POST':
        article.statut = 'brouillon'
        article.save()
        return redirect('blog')  # redirige vers la liste du blog

    return render(request, 'blog/confirmer_suppression.html', {'article': article})
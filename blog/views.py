from django.shortcuts import redirect, render, get_object_or_404
from .models import Article, Commentaire, Categorie, Tag
from .forms import CommentaireForm

def blog_list(request):
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        articles = Article.objects.filter(statut='publie', categorie__id=categorie_id)
    else:
        articles = Article.objects.filter(statut='publie')
    blog_categories = Categorie.objects.all()  # Ou un queryset spécifique pour le blog
    context = {
        'articles': articles,
        'blog_categories': blog_categories,
    }
    return render(request, 'blog/blog.html', context)

def single_blog(request, pk):
    article = get_object_or_404(Article, pk=pk)
    commentaires = article.commentaires.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentaireForm(request.POST)
            if form.is_valid():
                commentaire = form.save(commit=False)
                commentaire.utilisateur = request.user
                commentaire.article = article
                commentaire.save()
                return redirect('single_blog', pk=article.pk)
        else:
            return redirect('login')
    else:
        form = CommentaireForm()
    recent_posts = Article.objects.filter(statut='publie').exclude(pk=article.pk).order_by('-date_publication')[:4]
    return render(request, 'blog/single-blog.html', {
        'article': article,
        'recent_posts': recent_posts,
        'commentaires': commentaires,
        'form': form
    })


def blog_by_tag(request, slug):
    tag = get_object_or_404(Tag, nom=slug)
    articles = Article.objects.filter(tags=tag, statut='publie')
    return render(request, 'blog/blog.html', {'articles': articles, 'selected_tag': tag})



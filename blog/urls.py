from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog'),
    path('article/<int:pk>/', views.single_blog, name='single_blog'),
    path('tag/<slug:slug>/', views.blog_by_tag, name='blog_by_tag'),
    path('ajouter/', views.ajouter_article_blog, name='ajouter_article_blog'),
    path('modifier/<int:article_id>/', views.modifier_article, name='modifier_article'),
    path('supprimer/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
]

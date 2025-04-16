# Generated by Django 5.2 on 2025-04-15 09:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_article_contenu'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reponses', to='blog.commentaire'),
        ),
    ]

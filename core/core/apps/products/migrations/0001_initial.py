# Generated by Django 4.2 on 2023-05-14 20:33

import core.apps.products.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_cku', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='categorie')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=150, null=True, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.apps.products.models.upload_image_path)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='date de creation')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.apps.products.models.upload_image_path)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='date de creation')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
            ],
            options={
                'verbose_name': 'categorie',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cku', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('reference', models.CharField(editable=False, max_length=10, unique=True)),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Article')),
                ('slug', models.SlugField(blank=True, editable=False, null=True, unique=True)),
                ('overview', models.CharField(default='', help_text="petite description de l'article", max_length=180)),
                ('description', tinymce.models.HTMLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MaxValueValidator(1000000000000), django.core.validators.MinValueValidator(100)], verbose_name='prix')),
                ('image', models.ImageField(upload_to=core.apps.products.models.upload_image_path)),
                ('is_active', models.BooleanField(default=True, verbose_name='Disponible ?')),
                ('in_stock', models.BooleanField(default=True, verbose_name='En stock ?')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='date ajout')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category', verbose_name='categorie')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
    ]
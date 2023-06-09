# Generated by Django 4.2 on 2023-05-19 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, max_length=350, null=True, verbose_name='adresse ip')),
                ('session_key', models.CharField(blank=True, max_length=150, null=True, verbose_name='clé session')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='date de creation')),
                ('active', models.BooleanField(default=True, verbose_name='activé')),
                ('ended', models.BooleanField(default=False, verbose_name='session terminée')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='client')),
            ],
            options={
                'verbose_name': 'Session client',
                'verbose_name_plural': 'Sessions client',
            },
        ),
        migrations.CreateModel(
            name='ObjectView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, max_length=350, null=True, verbose_name='adresse ip du client')),
                ('object_id', models.PositiveIntegerField(verbose_name='identifiant')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='consulté le ')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='contenu')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='client')),
            ],
            options={
                'verbose_name': 'Objet Vue',
                'verbose_name_plural': 'Objets Vues',
                'ordering': ('-timestamp',),
            },
        ),
    ]

# Generated by Django 4.2 on 2023-05-20 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adresse',
            options={'ordering': ('-id',), 'verbose_name': 'Differente adresse', 'verbose_name_plural': 'Differentes adresses'},
        ),
    ]

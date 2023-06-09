# Generated by Django 4.2 on 2023-05-19 16:45

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.URLField(blank=True, max_length=300, null=True, verbose_name='Facebook')),
                ('instagram', models.URLField(blank=True, max_length=300, null=True, verbose_name='Instagram')),
                ('twitter', models.URLField(blank=True, max_length=300, null=True, verbose_name='Twitter')),
                ('whatsapp', models.URLField(blank=True, max_length=300, null=True, verbose_name='WhatsApp')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Téléphone')),
                ('email', models.EmailField(default='example@gmail.com', max_length=254)),
                ('address', models.TextField(default='Conakry', verbose_name='adresse')),
            ],
            options={
                'verbose_name': 'Reseau social',
                'verbose_name_plural': 'Reseaux sociaux',
            },
        ),
    ]

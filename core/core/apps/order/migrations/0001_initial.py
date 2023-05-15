# Generated by Django 4.2 on 2023-05-14 20:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=150, verbose_name='N° commande')),
                ('status', models.CharField(choices=[('created', 'créer'), ('paid', 'payer'), ('shipped', 'livrer'), ('refunded', 'rembourser')], default='created', max_length=150)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=9.99, max_digits=100, verbose_name='frais de livraison')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100, verbose_name='total')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date de creation')),
                ('active', models.BooleanField(default=True)),
                ('billing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.billingprofile', verbose_name='client')),
            ],
            options={
                'verbose_name': 'Commande',
                'verbose_name_plural': 'Commandes',
            },
        ),
    ]

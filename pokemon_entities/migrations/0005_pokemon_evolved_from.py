# Generated by Django 2.2.6 on 2020-08-11 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_auto_20200811_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolved_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokemon_entities.Pokemon', verbose_name='Эволлюционировал из'),
        ),
    ]

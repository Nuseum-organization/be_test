# Generated by Django 4.0.6 on 2022-08-03 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('energy', models.FloatField(default=0.0)),
                ('carbohydrate', models.FloatField(default=0.0)),
                ('protein', models.FloatField(default=0.0)),
                ('fat', models.FloatField(default=0.0)),
                ('dietary_fiber', models.FloatField(default=0.0)),
                ('magnesium', models.FloatField(default=0.0)),
                ('vitamin_c', models.FloatField(default=0.0)),
                ('vitamin_d', models.FloatField(default=0.0)),
                ('vitamin_b6', models.FloatField(default=0.0)),
                ('vitamin_b12', models.FloatField(default=0.0)),
                ('folic_acid', models.FloatField(default=0.0)),
                ('tryptophan', models.FloatField(default=0.0)),
                ('dha_epa', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(blank=True, to='foods.category')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 4.0.6 on 2022-08-19 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_rename_food_id_consumption_food_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Consumption',
        ),
    ]

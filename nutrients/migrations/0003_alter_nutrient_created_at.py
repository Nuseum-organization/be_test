# Generated by Django 4.0.6 on 2022-08-17 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrients', '0002_rename_vitamin_c_nutrient_vitamin_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrient',
            name='created_at',
            field=models.CharField(max_length=10),
        ),
    ]

# Generated by Django 4.0.6 on 2022-08-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_rename_vitamin_c_food_vitamin_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
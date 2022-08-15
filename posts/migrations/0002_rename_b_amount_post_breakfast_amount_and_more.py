# Generated by Django 4.0.6 on 2022-08-15 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0005_remove_category_slug_food_classifier_and_more'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='b_amount',
            new_name='breakfast_amount',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='d_amount',
            new_name='dinner_amount',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='l_amount',
            new_name='lunch_amount',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='s_amount',
            new_name='snack_amount',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AddField(
            model_name='post',
            name='supplement',
            field=models.ManyToManyField(blank=True, related_name='supplement_food', to='foods.food'),
        ),
        migrations.AddField(
            model_name='post',
            name='supplement_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

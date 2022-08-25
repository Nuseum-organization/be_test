# Generated by Django 4.0.6 on 2022-08-23 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_created_at'),
        ('consumptions', '0004_remove_waterconsumption_deprecated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumption',
            name='img1',
        ),
        migrations.RemoveField(
            model_name='consumption',
            name='img2',
        ),
        migrations.RemoveField(
            model_name='consumption',
            name='img3',
        ),
        migrations.CreateModel(
            name='FoodImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='post/images/%Y/%m/%d')),
                ('meal_type', models.CharField(choices=[('breakfast', '아침'), ('lunch', '점심'), ('dinner', '저녁'), ('snack', '간식')], default=' ', max_length=12)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
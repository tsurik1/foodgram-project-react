# Generated by Django 4.1.7 on 2023-05-20 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='img_recipe/', verbose_name='Загрузить фото'),
        ),
    ]

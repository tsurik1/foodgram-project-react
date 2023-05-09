# Generated by Django 4.1.7 on 2023-04-22 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipeingredient_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='ingridient',
            new_name='ingredient',
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='рецепт'),
        ),
    ]

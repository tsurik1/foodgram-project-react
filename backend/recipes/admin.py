from django.contrib import admin

from .models import (Ingredient,
                     Recipe,
                     RecipeIngredient,
                     Tag,
                     ShoppingCart,
                     Favorite,
                     )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'amount')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('text',)
    readonly_fields = ('favorites_count',)
    inlines = (RecipeIngredientInline,)

    def favorites_count(self, obj):
        return obj.in_favorite.count()
    favorites_count.short_description = 'Количество добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('slug',)}


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)

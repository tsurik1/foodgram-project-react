from django.contrib import admin

from .models import Recipe, Tag, Ingredient, Favourite, ShoppingCart, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient

@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author')
    search_fields = ('text',)
    empty_value_display = '-пусто-'
    inlines = [RecipeIngredientInline]


class TagsAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name', 'slug')


class FavouriteAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'recipe', 'user')

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'recipe', 'amount')

# @admin.register(RecipeIngredient)
# class RecipeIngredientAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'amount')
# @admin.register(Tags)
# class TagsAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     pass
# class RecipeIngredientInline(admin.TabularInline):
#     model = RecipeIngredient

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'display_genre')
#     inlines = [BooksInstanceInline]

admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredient)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(ShoppingCart)

from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

admin.register(Category)
admin.register(Genre)
admin.register(Title)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review', 'author')
    list_filter = ('review', 'author', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('title', 'author', 'pub_date')
    list_filter = ('author', 'score', 'pub_date')
    empty_value_display = '-пусто-'

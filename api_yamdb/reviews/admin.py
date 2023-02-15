from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User

admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'score',
        'author',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'


class GenreTitleInline(admin.StackedInline):
    model = GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [GenreTitleInline]
    list_display = (
        'name',
        'year',
        'description',
        'category',
        'get_genre',
    )
    search_fields = ('name',)
    list_filter = ('name', 'category')
    list_editable = ('category',)
    empty_value_display = '-empty-'

    def get_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username', 'role',)
    list_editable = ('role',)
    empty_value_display = '-empty-'

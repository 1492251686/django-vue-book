from django.contrib import admin
from .models import BookLists, ChapterLists, BookClassification, BookSource
# Register your models here.

admin.site.site_header = "南山书院"
admin.site.index_title = "管理后台"


@admin.register(BookClassification)
class BookClassificationAdmin(admin.ModelAdmin):
    change_list_template = "BookClass/book_class.html"
    list_display = ['name', 'url', 'book_number', 'sort', 'num', 'add_books']
    list_editable = ['sort', 'num']


@admin.register(BookLists)
class BookListAdmin(admin.ModelAdmin):
    add_form_template = "BookList/search_book.html"
    change_list_template = "BookList/book_lists.html"
    list_display = ['name', 'author', 'show_cover', 'url', 'newest_chapter', 'last_update_time', 'chapter_num', 'create_time','class_ification', 'buttons', 'target_chpter']
    search_fields = ['name', 'author']
    list_filter = ['create_time']
    list_per_page = 20

    def class_ification(self, obj):
        return obj.classification.name
    class_ification.short_description = "分类"


@admin.register(ChapterLists)
class ChapterListAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'book_name', 'author_name']
    search_fields = ['book__name', 'book__author']
    list_per_page = 50

    def book_name(self, obj):
        return obj.book.name
    book_name.short_description = "书名"

    def author_name(self, obj):
        return obj.book.author
    author_name.short_description = "作者"


@admin.register(BookSource)
class BookSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'book_number']
    search_fields = ['name']
    list_per_page = 50
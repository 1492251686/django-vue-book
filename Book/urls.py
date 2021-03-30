from django.urls import path
from .views import search_book, add_search_book, update_book_chapter, batch_add_book, BookList
app_name = "Book"
urlpatterns = [
    path('search_book', search_book, name='search'),
    path('source_list', BookList.as_view(), name='source_list'),
    path('add_book', add_search_book, name='add_book'),
    path('update_chapter', update_book_chapter, name='update_chapter'),
    path('batch_add_book', batch_add_book, name='batch_add_book'),
]
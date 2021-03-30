from django.urls import path
from . import views
app_name = "api"
urlpatterns = [
    path('chapter/', views.Chapter.as_view()),
    path('chapter_list/', views.ChapterList.as_view()),
    path('search_book/', views.BookList.as_view()),
    path('send_email/', views.SendEmail.as_view()),
    # path('info_chapter_list/', views.InfoChapterList.as_view())
]

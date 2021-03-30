from django.urls import path
from . import views
app_name = "Web"
urlpatterns = [
    path('', views.web_index),
]

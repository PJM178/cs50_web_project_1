from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_to_wiki, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/<str:name>", views.title, name = "title"),
    path("wiki/new_page/", views.new_page, name="new_page"),
    path("wiki/random_page/", views.random_page, name="random"),
    ]

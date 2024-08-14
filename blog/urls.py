from django.urls import path
from .views import *
urlpatterns = [
    path("", Blogpage, name="Blogpage"),
    path("Postpage/<str:title>/", Postpage, name="Postpage"),
    path("post_comment/", post_comment, name="post_comment"),
    path("search_view/", search_view, name="search_view"),
    path("get_category/<str:cat>/", get_category, name="get_category"),
]

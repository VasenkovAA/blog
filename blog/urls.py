from django.urls import path

from blog.views.index import index
from blog.views.post import post_detail, post_list

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("blog/<int:id>/", post_detail, name="post_detail"),
    path("blog/list/", post_list, name="post_list"),
]

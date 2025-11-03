from django.urls import path

from blog.views.index import index
from blog.views.post import post_comment, post_detail, post_list

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("blog/list/", post_list, name="post_list"),
    path(
        "blog/<int:year>/<int:month>/<int:day>/<slug:post>/",
        post_detail,
        name="post_detail",
    ),
    path("blog/<int:post_id>/comment/", post_comment, name="post_comment"),
    path("blog/tag/<slug:tag_slug>/", post_list, name="post_list_by_tag"),
]

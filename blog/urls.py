from django.urls import path

from blog.views.index import index

urlpatterns = [
    path("", index, name="index"),
]

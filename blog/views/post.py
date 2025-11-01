from django.shortcuts import get_object_or_404, render

from blog.models.post import Post


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, "post/detail.html", {"post": post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, "post/list.html", {"posts": posts})

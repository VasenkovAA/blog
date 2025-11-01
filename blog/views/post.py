from django.shortcuts import get_object_or_404, render

from blog.models.post import Post


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED,
    )
    return render(request, "post/detail.html", {"post": post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, "post/list.html", {"posts": posts})

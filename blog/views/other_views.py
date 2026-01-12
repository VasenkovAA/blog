from django.shortcuts import render


def about_me(request, tag_slug=None):
    return render(request, 'other/about_me.html')

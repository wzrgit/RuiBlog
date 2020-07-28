from django.shortcuts import render
from blog.views import common


def albums(request):
    # TODO check auth
    content = {'common': common.GetCommons()}
    return render(request, 'management/albums.html', content)

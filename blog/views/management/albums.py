from django.shortcuts import render
from blog.views import common


def albums(request):
    # TODO check auth
    content = {'common': common.get_commons(request)}
    return render(request, 'management/albums.html', content)

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .common import Common


def albums_list(request):
    common = Common.get_commons(request)
    content = {'common': common}
    return render(request, 'themes/' + common['theme'] + '/albums.html', content)


def album_view(request, album_id, curr_page=0):
    common = Common.get_commons(request)
    content = {'common': common}
    return render(request, 'themes/' + common['theme'] + '/albums.html', content)

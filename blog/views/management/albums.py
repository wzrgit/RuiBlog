from django.http import JsonResponse
from django.shortcuts import render
from blog.views import common
import json


def albums(request):
    # TODO check auth
    content = {'common': common.get_commons(request)}
    return render(request, 'management/albums.html', content)


def create_album(request):
    # if not request.user.is_authenticated:
    #     pass
    #
    # if request.method != 'POST':
    #     pass

    print(request.POST)
    return JsonResponse({}, safe=False)

from django.http import JsonResponse
from django.shortcuts import render
from blog.views.common import Common
from blog.models import Album
import datetime
import json


def albums(request):
    # TODO check auth
    content = {'common': Common.get_commons(request)}
    return render(request, 'management/albums.html', content)


def create_album(request):
    """
    :param request:
    :return:
    """
    # if not request.user.is_authenticated:
    #     pass
    #
    if request.method != 'POST':
        content = Common.get_response_content(False)
    else:
        try:
            print(request.POST)
            name = request.POST['album_name']
            desc = request.POST['album_desc']
            if 'is_show_exif' in request.POST:
                show_exif = True
            else:
                show_exif = False

            create_time = request.POST['create_time']
            if len(create_time) == 0:
                create_time = datetime.datetime.now()

            print(create_time)
            new_album = Album.objects.create(title=name, desc=desc, show_exif=show_exif, create_time=create_time,
                                             update_time=create_time)
            print('***')
            print(new_album)
            content = Common.get_response_content()
        except Exception as e:
            print(e)
            content = Common.get_response_content(False)
            content['error'] = str(e)

    return JsonResponse(content, safe=False)

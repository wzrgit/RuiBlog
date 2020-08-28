from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from blog.models import Album, Photos, VisitStatus
from .common import Common


def albums_list(request):
    if not request.user.is_authenticated:
        albums = Album.objects.all().order_by('-create_time').values()
    else:
        albums = Album.objects.filter(visit_status__in=[VisitStatus.Public, VisitStatus.Protected]).order_by(
            '-create_time').values()

    for album in albums:
        count = Photos.objects.all().count()
        album['count'] = count
        if count > 0:
            if not album.cover_img or len(album.cover_img) == 0:
                cover = Photos.objects.filter(album_id=album.id).order_by('-create_time')[0]

    albums = list(filter(lambda a: a['count'] != 0, albums))

    common = Common.get_commons(request)
    content = {'common': common,
               'albums': albums}

    return render(request, 'themes/' + common['theme'] + '/albums.html', content)


def album_view(request, album_id, curr_page=0):
    common = Common.get_commons(request)
    content = {'common': common}
    return render(request, 'themes/' + common['theme'] + '/albums.html', content)

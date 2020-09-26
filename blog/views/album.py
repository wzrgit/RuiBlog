from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from blog.models import Album, Photos, VisitStatus
import RuiBlog.settings as blog_settings
from .common import Common
import json


def get_hard_album_path(album_id):
    return blog_settings.MEDIA_ROOT + blog_settings.PHOTO_PATH_PREFIX + str(album_id)


def photo_make_path(photo):
    photo['path'] = blog_settings.PHOTO_PATH_PREFIX + str(photo['album_id']) + '/' + photo['name']
    photo['thumb_m'] = blog_settings.PHOTO_PATH_PREFIX + str(photo['album_id']) + '/thumb_m/' + photo['name']
    photo['thumb_s'] = blog_settings.PHOTO_PATH_PREFIX + str(photo['album_id']) + '/thumb_s/' + photo['name']


def check_cover_img(album):
    if album['cover_img']:
        photo_id = album['cover_img']
        photo = Photos.objects.filter(id=photo_id).values()
        if len(photo) > 0:
            cover = photo[0]
            photo_make_path(cover)
            album['cover_img'] = cover
            return True

    photos = Photos.objects.filter(album_id=album['id']).order_by('create_time').values()
    if len(photos) > 0:
        cover = photos[0]
        photo_make_path(cover)
        album['cover_img'] = cover
        return True

    return False


def albums_list(request):
    if request.user.is_authenticated:
        albums = Album.objects.all().order_by('-create_time').values()
    else:
        albums = Album.objects.filter(visit_status__in=[VisitStatus.Public]).order_by(
            '-create_time').values()

    for album in albums:
        check_cover_img(album)
        count = len(Photos.objects.filter(album_id=album['id']))
        album['count'] = count

    albums = list(filter(lambda a: a['count'] != 0, albums))

    common = Common.get_commons(request)
    content = {'common': common,
               'albums': albums}

    return render(request, 'themes/' + common['theme'] + '/albums.html', content)


def album_view(request, album_id, curr_page=0):
    # TODO check album can be access
    common = Common.get_commons(request)
    album = Album.objects.get(id=album_id)
    photos = Photos.objects.filter(album_id=album_id).order_by('-create_time').values()
    for p in photos:
        photo_make_path(p)
        if p['exif']:
            p['exif'] = json.loads(p['exif'])

    content = {'common': common,
               'photos': photos,
               'album': album}

    return render(request, 'themes/' + common['theme'] + '/album_view.html', content)

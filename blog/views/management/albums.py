from django.http import JsonResponse
from django.shortcuts import render
from blog.views.common import Common
from blog.models import Album, Photos, VisitStatus
from blog.views.management.forms import FormAlbumMeta, FormUploadImage
import datetime
import json


def albums(request):
    # TODO check auth
    content = {'common': Common.get_commons(request),
               'albums': Album.objects.all().order_by('-create_time').values()}

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
            name = request.POST['album_name']
            desc = request.POST['album_desc']
            if 'is_show_exif' in request.POST:
                show_exif = True
            else:
                show_exif = False

            create_time = request.POST['create_time']
            if len(create_time) == 0:
                create_time = datetime.datetime.now()

            new_album = Album.objects.create(title=name, desc=desc, show_exif=show_exif, create_time=create_time,
                                             update_time=create_time)

            content = Common.get_response_content()
        except Exception as e:
            print(e)
            content = Common.get_response_content(False)
            content['error'] = str(e)

    return JsonResponse(content, safe=False)


def edit_album(request, album_id):
    common = Common.get_commons(request)
    if request.method == "GET":
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Common.redirect_to_404(request)

        default_data = {'f_id': album.id,
                        'f_title': album.title,
                        'f_desc': album.desc,
                        'f_show_exif': album.show_exif,
                        'f_visit_status': album.visit_status,
                        'f_pwd': album.password,
                        'f_create_time': album.create_time}

        form = FormAlbumMeta(default_data)

        form.fields['f_id'].widget.attrs.update({'readonly': 'readonly'})
        form.fields['f_id'].widget.attrs['class'] += ' d-none'

        form_photo = FormUploadImage()
        photos = Photos.objects.filter(album_id=album_id).values()

        content = {'common': common,
                   'album_meta_form': form,
                   'upload_photo_form': form_photo,
                   'photos': photos
                   }
        return render(request, 'management/album_edit.html', content)

    elif request.method == "POST":
        return update_album(request, album_id)


def update_album(request, album_id):
    """
    JSON interface
    :param request:
    :param album_id:
    :return:
    """

    ret = True
    error = ""

    form = FormAlbumMeta(request.POST)
    if not form.is_valid():
        ret = False
        error = form.errors

    f_id = form.cleaned_data['f_id']
    f_title = form.cleaned_data['f_title']
    f_desc = form.cleaned_data['f_desc']
    f_show_exif = form.cleaned_data['f_show_exif']
    f_visit_status = form.cleaned_data['f_visit_status']
    f_pwd = form.cleaned_data['f_pwd']
    f_create_time = form.cleaned_data['f_create_time']

    if album_id != f_id:
        ret = False
        error = "album_id error"

    if f_visit_status == VisitStatus.Protected and len(f_pwd) == 0:
        ret = False
        error = "password must not empty when album is protected"

    else:
        try:
            album = Album.objects.filter(id=album_id).update(title=f_title,
                                                             desc=f_desc,
                                                             show_exif=f_show_exif,
                                                             visit_status=f_visit_status,
                                                             password=f_pwd,
                                                             create_time=f_create_time)
        except Exception as e:
            error = e

    content = Common.get_response_content(ret)
    content['error'] = error
    return JsonResponse(content, safe=False)


def upload_photo(request, album_id):
    """
    JSON interface
    :param request:
    :param album_id:
    :return:
    """
    pass


def update_photo(request, photo_id):
    """
    JSON interface
    :param request:
    :param photo_id:
    :return:
    """
    pass

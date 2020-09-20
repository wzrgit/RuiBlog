from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from blog.views.common import Common
from blog.views import album as view_album
from blog.models import Album, Photos, VisitStatus
from blog.views.management.forms import FormAlbumMeta, FormUploadImage
import RuiBlog.settings as blog_settings
import datetime
import os
from PIL import Image, ExifTags
import json


@login_required
def albums(request):
    albums_lst = Album.objects.all().order_by('-create_time').values()
    for album in albums_lst:
        view_album.check_cover_img(album)

    # TODO check cover_img
    content = {'common': Common.get_commons(request),
               'albums': albums_lst}

    return render(request, 'management/albums.html', content)


@login_required
def create_album(request):
    """
    :param request:
    :return:
    """

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


@login_required
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
        photos = Photos.objects.filter(album_id=album_id).order_by('-create_time').values()
        for p in photos:
            view_album.photo_make_path(p)

        content = {'common': common,
                   'album_meta_form': form,
                   'upload_photo_form': form_photo,
                   'photos': photos,
                   'album_id': album_id
                   }
        return render(request, 'management/album_edit.html', content)

    elif request.method == "POST":
        return update_album(request, album_id)


@login_required
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


@login_required
def upload_photo(request, album_id):
    if request.method != "POST":
        return HttpResponseBadRequest()

    form = FormUploadImage(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest()

    img_file = request.FILES['f_img']
    pic_name = img_file._get_name()
    tm = datetime.datetime.now()
    tmf = tm.strftime('%Y%m%d%H%M%S%f')[:-3]
    pic_name = tmf + '_' + pic_name

    album_path = view_album.get_hard_album_path(album_id)
    exif = handle_save_pic(album_path, pic_name, img_file)
    exif_str = json.dumps(exif, allow_nan=True)
    if '\x00' in exif_str:
        exif_str = exif_str.replace('\x00', '')
    if '\u0000' in exif_str:
        exif_str = exif_str.replace('\u0000', '')

    alias = form.cleaned_data['f_alias']
    if not alias:
        alias = img_file._get_name()
    desc = form.cleaned_data['f_desc']

    Photos.objects.create(album_id=album_id, name=pic_name, alias=alias, desc=desc, exif=exif_str, create_time=tm,
                          update_time=tm)

    return HttpResponseRedirect(reverse('edit_album', args=[album_id]))


def check_folders(album_path):
    for p in [album_path, album_path + '/thumb_m', album_path + '/thumb_s']:
        if not os.path.exists(p):
            os.makedirs(p)


def handle_save_pic(album_path, file_name, img_file):
    check_folders(album_path)

    full_path = album_path + '/' + file_name
    with open(full_path, 'wb+') as destination:
        for chunk in img_file.chunks():
            destination.write(chunk)
    img = Image.open(img_file)
    exif = get_exif(img)
    compress_thumb(img, album_path, file_name)
    img.close()

    return exif


def compress_thumb(img, album_path, file_name):
    if img.width > 600 and img.height > 600:
        if img.width > img.height:
            m = 600 * img.width / img.height
            s = 256 * img.width / img.height
        else:
            m = 600 * img.height / img.width
            s = 256 * img.height / img.width
        img.thumbnail((m, m))
        img.save(album_path + '/thumb_m/' + file_name)
        img.thumbnail((s, s))
        img.save(album_path + '/thumb_s/' + file_name)
    else:
        img.save(album_path + '/thumb_m/' + file_name)
        img.save(album_path + '/thumb_s/' + file_name)


def get_exif(img):
    info = img._getexif()
    if not info:
        return {}
    tg = {}
    for tag, value in info.items():
        decoded = ExifTags.TAGS.get(tag, tag)
        tg[decoded] = value
    ret_obj = {}
    ret_obj['Model'] = tg.get('Model')
    ret_obj['LensModel'] = tg.get('LensModel')
    if 'FNumber' in tg:
        ret_obj['FNumber'] = float(tg['FNumber'])
    if 'FocalLength' in tg:
        ret_obj['FocalLength'] = float(tg['FocalLength'])
    if 'ExposureTime' in tg:
        ret_obj['ExposureTime'] = float(tg['ExposureTime'])
    ret_obj['ISOSpeedRatings'] = tg.get('ISOSpeedRatings')

    return ret_obj


def update_photo(request):
    """
    JSON interface
    :param request:
    :return:
    """
    if request.method != 'POST':
        ret = Common.get_response_content(False)
    else:
        photo_id = request.POST.get('photo_id')
        alias = request.POST.get('alias')
        desc = request.POST.get('desc')

        if not photo_id or int(photo_id) < 0:
            ret = Common.get_response_content(False)
        else:
            if not (alias is None):
                Photos.objects.filter(id=photo_id).update(alias=alias)
            if not (desc is None):
                Photos.objects.filter(id=photo_id).update(desc=desc)
            ret = Common.get_response_content(True)

    return JsonResponse(ret, safe=False)


@login_required
def delete_photo(request):
    """
    JSON interface
    :param request:
    :return:
    """
    if request.method != 'POST':
        ret = Common.get_response_content(False)

    photo_id = request.POST.get('photo_id')
    album_id = request.POST.get('album_id')
    if not (photo_id or albums):
        return JsonResponse(Common.get_response_content(False), safe=False)

    photo = Photos.objects.filter(id=photo_id)
    if len(list(photo)) != 1:
        ret = Common.get_response_content()
    else:
        p = list(photo.values())[0]
        view_album.photo_make_path(p)
        photo.delete()
        os.remove(blog_settings.MEDIA_ROOT + p['path'])
        os.remove(blog_settings.MEDIA_ROOT + p['thumb_m'])
        os.remove(blog_settings.MEDIA_ROOT + p['thumb_s'])
        ret = Common.get_response_content()

    return JsonResponse(ret, safe=False)

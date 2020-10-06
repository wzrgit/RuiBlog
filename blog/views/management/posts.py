from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog.views.common import Common
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus, TrashStatus, PostCovers
from blog.views.management import albums
from .forms import FormPost
import datetime
import blog.views.posts as posts_view


@login_required
def posts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin:login'))

    post_metas = Posts.objects.values('id', 'title', 'subtitle', 'public_time', 'visit_status',
                                      'trash_status', 'cover').order_by('-public_time')
    for p in post_metas:
        categories = CategoryHasPosts.objects.filter(post_id=p['id'])
        p['categories'] = categories.values()
        if len(p['cover']) > 0:
            cover_img = PostCovers.objects.filter(id=int(p['cover'])).values()[0]
            posts_view.check_cover(cover_img)
            p['cover_img'] = cover_img

    normal_posts = Posts.objects.filter(trash_status=TrashStatus.Normal)
    trashed_posts = Posts.objects.filter(trash_status=TrashStatus.Trashed)

    counts = {'all': Posts.objects.count(),
              'publish': normal_posts.filter(visit_status=VisitStatus.Public).count(),
              'protected': normal_posts.filter(visit_status=VisitStatus.Protected).count(),
              'private': normal_posts.filter(visit_status=VisitStatus.Private).count(),
              'draft': normal_posts.filter(visit_status=VisitStatus.Draft).count(),
              'deleted': trashed_posts.count(),
              }

    content = {'common': Common.get_commons(request),
               'counts': counts,
               'post_metas': post_metas,
               }
    return render(request, 'management/posts.html', content)


@login_required
def edit_post(request, post_id=-1):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin:login') + '?%s=%s' % ('next', request.path))

    cover_id = None
    if request.method == 'GET':
        form = FormPost()
        form.update_placeholder(['f_title', 'f_subtitle'])

        if post_id == -1:
            form.fields['f_pwd'].widget.attrs.update({'readonly': 'readonly'})
            for f in ['f_create_tm', 'f_publish_tm', 'f_update_tm']:
                form.fields[f].initial = timezone.now()

        else:
            pts = Posts.objects.filter(id=post_id)
            if len(pts) > 0:
                post = pts[0]
                cover_id = post.cover
                default_data = {'f_id': post.id,
                                'f_title': post.title,
                                'f_subtitle': post.subtitle,
                                'f_create_tm': post.create_time,
                                'f_publish_tm': post.public_time,
                                'f_update_tm': post.update_time,
                                'f_content': post.content,
                                'f_visit_status': post.visit_status,
                                'f_comment_status': post.comment_status,
                                'f_pwd': post.password,
                                'f_cover': post.cover,
                                }
                form = FormPost(default_data)
            else:
                raise ValueError

        for f in ['f_id', 'f_create_tm', 'f_update_tm', 'f_cover']:
            form.fields[f].widget.attrs.update({'readonly': 'readonly'})
            form.fields[f].widget.attrs['class'] += ' d-none'

    elif request.method == 'POST':
        form = FormPost(request.POST)
        if not form.is_valid():
            print(form.errors)
            raise ValueError
        else:
            f_id = form.cleaned_data['f_id']
            f_title = form.cleaned_data['f_title']
            f_sub_title = form.cleaned_data['f_subtitle']
            f_create_tm = form.cleaned_data['f_create_tm']
            f_publish_tm = form.cleaned_data['f_publish_tm']
            f_up_tm = form.cleaned_data['f_update_tm']
            f_visit = form.cleaned_data['f_visit_status']
            f_pwd = form.cleaned_data['f_pwd']
            f_can_comment = form.cleaned_data['f_comment_status']
            f_content = form.cleaned_data['f_content']
            f_cover = form.cleaned_data['f_cover']

            if f_id == -1:
                post = Posts.objects.create(title=f_title,
                                            subtitle=f_sub_title,
                                            create_time=f_create_tm,
                                            public_time=f_publish_tm,
                                            update_time=timezone.now(),
                                            visit_status=f_visit,
                                            password=f_pwd,
                                            comment_status=f_can_comment,
                                            content=f_content,
                                            cover=f_cover,
                                            author=request.user.id)
                pid = post.id
            else:
                post = Posts.objects.filter(id=f_id).update(title=f_title,
                                                            subtitle=f_sub_title,
                                                            create_time=f_create_tm,
                                                            public_time=f_publish_tm,
                                                            update_time=timezone.datetime.now(),
                                                            visit_status=f_visit,
                                                            password=f_pwd,
                                                            cover=f_cover,
                                                            comment_status=f_can_comment,
                                                            content=f_content)
                pid = post_id
            return HttpResponseRedirect(reverse('edit_post', kwargs={'post_id': pid}))

    # get cover
    if cover_id:
        cover = PostCovers.objects.filter(id=cover_id).values()[0]
        posts_view.check_cover(cover)
    else:
        cover = None
    content = {'common': Common.get_commons(request),
               'form': form,
               'cover': cover}

    return render(request, 'management/post_edit.html', content)


@login_required
def get_post_id_from_post(request):
    """
    get post_id from request
    :param request:
    :return: -1 if error
    """
    pid = -1
    ret = Common.get_response_content(False)
    if request.method != 'POST':
        return pid

    post_id = request.POST.get('post_id')
    if post_id is None or (not post_id.isnumeric()):
        return pid

    return int(post_id)


@login_required
def remove_post_to_trash(request):
    post_id = get_post_id_from_post(request)
    if post_id == -1:
        return JsonResponse(Common.get_response_content(False), safe=False)
    Posts.objects.filter(id=post_id).update(trash_status=TrashStatus.Trashed)
    return JsonResponse(Common.get_response_content(), safe=False)


@login_required
def recover_post_from_trash(request):
    post_id = get_post_id_from_post(request)
    if post_id == -1:
        return JsonResponse(Common.get_response_content(False), safe=False)
    Posts.objects.filter(id=post_id).update(trash_status=TrashStatus.Normal)
    return JsonResponse(Common.get_response_content(), safe=False)


@login_required
def destroy_post(request):
    post_id = get_post_id_from_post(request)
    if post_id == -1:
        return JsonResponse(Common.get_response_content(False), safe=False)

    post = Posts.objects.filter(id=post_id).values()
    if len(post) <= 0 or post[0]['trash_status'] != TrashStatus.Trashed:
        pass  # TODO log or waning

    Posts.objects.filter(id=post_id).delete()
    return JsonResponse(Common.get_response_content(), safe=False)


@login_required
def upload_post_cover(request):
    if request.method != 'POST':
        return JsonResponse(Common.get_response_content(False), safe=False)

    img_file = request.FILES['f_img']
    img_name = img_file._get_name()
    tm = datetime.datetime.now()
    tmf = tm.strftime('%Y%m%d%H%M%S%f')[:-3]
    img_name = tmf + '_' + img_name
    path = posts_view.get_post_cover_hard_path(tm.strftime('%Y'))
    albums.handle_save_pic(path, img_name, img_file)
    PostCovers.objects.create(name=img_name, alias=img_file._get_name(), creation_time=tm)

    return JsonResponse(Common.get_response_content(), safe=False)


@login_required
def get_post_covers(request):
    covers = PostCovers.objects.all().order_by('-creation_time').values()
    ret = Common.get_response_content()
    for c in covers:
        posts_view.check_cover(c)
    ret['covers'] = covers

    common = Common.get_commons(request)
    common['covers'] = covers
    # return JsonResponse(ret, safe=False)
    return render(request, 'management/post_edit_covers.html', common)


@login_required
def del_post_cover(request):
    pass

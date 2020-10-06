from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus, TrashStatus, PostCovers
import RuiBlog.settings as blog_settings
from .common import Common
import re


def get_post_cover_hard_path(year):
    return blog_settings.MEDIA_ROOT + blog_settings.POST_COVER_PREFIX + year + '/'


def get_post_cover_soft_path(year):
    return blog_settings.POST_COVER_PREFIX + year + '/'


def check_cover(cover):
    tm = cover['creation_time']
    year = tm.strftime('%Y')
    cover['path'] = get_post_cover_soft_path(year) + cover['name']
    cover['thumb_m'] = get_post_cover_soft_path(year) + 'thumb_m/' + cover['name']
    cover['thumb_s'] = get_post_cover_soft_path(year) + 'thumb_s/' + cover['name']


def post_list(request, curr_page=0, category=-1):
    posts_per_page = 5
    text_length = 300

    from_num = int(curr_page) * posts_per_page
    to_num = from_num + posts_per_page
    if request.user.is_authenticated:
        posts = Posts.objects.values('id', 'title', 'subtitle', 'public_time', 'visit_status', 'cover',
                                     'content').exclude(visit_status=VisitStatus.Draft,
                                                        trash_status=TrashStatus.Trashed).order_by('-public_time')[
                from_num: to_num]
    else:
        posts = Posts.objects.values('id', 'title', 'subtitle', 'public_time', 'visit_status', 'cover',
                                     'content').filter(visit_status__in=[VisitStatus.Public],
                                                       trash_status__in=[TrashStatus.Normal]).order_by('-public_time')[
                from_num: to_num]

    for p in posts:
        if len(p['content']) > 300:
            p['content'] = p['content'][:300]

        if len(p['cover']) > 0:
            cover_img = PostCovers.objects.filter(id=int(p['cover'])).values()[0]
            check_cover(cover_img)
            p['cover_img'] = cover_img

        if request.user.is_authenticated:
            pass
        else:
            if p['visit_status'] != VisitStatus.Public:
                p['content'] = ''

        ctt = p['content']
        ctt = re.sub('</p>', '&nbsp;&nbsp;&nbsp;', ctt)
        # ctt = re.sub(r'<(\/)?([A-z0-9 ][^\>]*)*>(.*?)', ' ', ctt)
        ctt = re.sub('<[^>]*>', '', ctt)
        if len(ctt) > 600:
            max_len = 600
            idx = ctt.find('&nbsp;', max_len - 6, max_len)
            if idx > 0:
                max_len = idx
            ctt = ctt[:max_len]
        p['content'] = ctt

    categories = PostCategory.objects.all().values()

    content = {'common': Common.get_commons(request),
               'posts': posts,
               'categories': categories}

    theme = Common.get_commons(request)['theme']
    assert len(theme) > 0

    return render(request, 'themes/' + theme + '/posts.html', content)


def post_view(request, post_id):
    common = Common.get_commons(request)
    try:
        pt = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return HttpResponseRedirect('404.html')

    if not request.user.is_authenticated:
        if pt.visit_status in [VisitStatus.Private, VisitStatus.Draft]:
            return HttpResponseRedirect(reverse('admin:login'))
        elif pt.visit_status == VisitStatus.Protected:  # TODO check password
            return HttpResponseRedirect(reverse('admin:login'))

    content = {'common': common,
               'post': pt}

    return render(request, 'themes/' + common['theme'] + '/post_view.html', content)

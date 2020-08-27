from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus
from .common import Common


def post_list(request, curr_page=0, category=-1):
    posts_per_page = 5
    text_length = 300

    from_num = int(curr_page) * posts_per_page
    to_num = from_num + posts_per_page
    if request.user.is_authenticated:
        posts = Posts.objects.values('id', 'title', 'subtitle', 'public_time', 'visit_status', 'cover',
                                     'content').exclude(visit_status=VisitStatus.Draft).order_by('-public_time')[
                from_num: to_num]
    else:
        posts = Posts.objects.values('id', 'title', 'subtitle', 'public_time', 'visit_status', 'cover',
                                     'content').filter(
            visit_status__in=(VisitStatus.Public, VisitStatus.Protected)).order_by('-public_time')[from_num: to_num]

    for p in posts:
        if request.user.is_authenticated:
            if len(p['content']) > 300:
                p['content'] = p['content'][:300]
        else:
            if p['visit_status'] == VisitStatus.Public:
                if len(p['content']) > 300:
                    p['content'] = p['content'][:300]
            else:
                p['content'] = ''

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
        if pt.visit_status == VisitStatus.Protected:
            pass

    content = {'common': common,
               'post': pt}

    return render(request, 'themes/' + common['theme'] + '/post_view.html', content)

from django.shortcuts import render
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus
from .common import Common


def post_list(request, curr_page=0, category=-1):
    posts_per_page = 5

    from_num = int(curr_page) * posts_per_page
    to_num = from_num + posts_per_page
    if request.user.is_authenticated:
        posts = Posts.objects.values('id', 'title', 'subtitle', 'public_time', 'visit_status', 'cover').exclude(
            visit_status=VisitStatus.Draft).order_by('-public_time')[from_num: to_num]
    else:
        posts = Posts.objects.values('id', 'title', 'subtitle', 'public_time', 'visit_status', 'cover').filter(
            visit_status__in=(VisitStatus.Public, VisitStatus.Protected)).order_by('-public_time')[from_num: to_num]

    categories = PostCategory.objects.all()

    content = {'common': Common.get_commons(request),
               'posts': posts}

    theme = Common.get_commons(request)['theme']
    assert len(theme) > 0

    return render(request, 'themes/' + theme + '/posts.html', content)

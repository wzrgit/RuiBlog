from django.http import HttpRequest
from django.shortcuts import render
from blog.models import Options, Posts, PostCategory, Album, Photos
from blog.views import common


def dashboard(request):
    # TODO check auth
    recent_posts = Posts.objects.values('id', 'public_time', 'title', 'subtitle').order_by('-public_time')[0:5]
    counts = {'posts': Posts.objects.count(),
              'albums': Album.objects.count()}
    content = {'common': common.Common.get_commons(request),
               'counts': counts,
               'recent_posts': recent_posts}
    return render(request, 'management/dashboard.html', content)

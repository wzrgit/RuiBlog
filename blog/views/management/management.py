from django.http import HttpRequest
from django.shortcuts import render
from blog.models import Options, Posts, PostCategory, Album, Photos
from blog.views import common


def dashboard(request):
    # TODO check auth
    counts = {'posts': Posts.objects.count(),
              'albums': Album.objects.count()}
    content = {'common': common.GetCommons(),
               'counts': counts}
    return render(request, 'management/dashboard.html', content)

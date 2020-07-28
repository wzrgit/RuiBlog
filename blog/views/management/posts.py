from django.http import HttpRequest
from django.shortcuts import render
from blog.views import common
from blog.models import Posts, PostCategory, CategoryHasPosts


def posts(request):
    # TODO check auth
    counts = {'all': Posts.objects.count(),
              'publish':  Posts.objects.filter(visit_status=Posts.VISIT_STATUS)}
    content = {'common': common.GetCommons()}
    return render(request, 'management/posts.html', content)

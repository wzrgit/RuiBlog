from django.http import HttpRequest
from django.shortcuts import render
from blog.views import common
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus


def posts(request):
    # TODO check auth
    counts = {'all': Posts.objects.count(),
              'publish': Posts.objects.filter(visit_status=VisitStatus.Public).count(),
              'protected': Posts.objects.filter(visit_status=VisitStatus.Protected).count(),
              'private': Posts.objects.filter(visit_status=VisitStatus.Protected).count(),
              'draft': Posts.objects.filter(visit_status=VisitStatus.Draft).count(),
              }
    content = {'common': common.get_commons(request),
               'counts': counts}
    return render(request, 'management/posts.html', content)

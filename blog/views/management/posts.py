from django.http import HttpRequest
from django.shortcuts import render
from blog.views.common import Common
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus


def posts(request):
    # TODO check auth
    counts = {'all': Posts.objects.count(),
              'publish': Posts.objects.filter(visit_status=VisitStatus.Public).count(),
              'protected': Posts.objects.filter(visit_status=VisitStatus.Protected).count(),
              'private': Posts.objects.filter(visit_status=VisitStatus.Protected).count(),
              'draft': Posts.objects.filter(visit_status=VisitStatus.Draft).count(),
              }
    content = {'common': Common.get_commons(request),
               'counts': counts}
    return render(request, 'management/posts.html', content)

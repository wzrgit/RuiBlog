from django.http import HttpRequest
from django.shortcuts import render
from blog.views.common import Common
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus
from .forms import CreatePost


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


def create_post(request):
    if request.method == 'GET':
        form = CreatePost()
        form.update_placeholder(['f_title','f_subtitle'])
        form.fields['f_comment_status'].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
    elif request.method == 'POST':
        form = CreatePost(request.POST)
    else:
        pass

    content = {'common': Common.get_commons(request),
               'form': form}

    return render(request, 'management/post_edit.html', content)

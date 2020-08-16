from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from blog.views.common import Common
from blog.models import Posts, PostCategory, CategoryHasPosts, VisitStatus
from .forms import FormPost


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


def edit_post(request, post_id=-1):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin:login') + '?%s=%s' % ('next', request.path))

    if request.method == 'GET':
        form = FormPost()
        form.update_placeholder(['f_title', 'f_subtitle'])

        if post_id == -1:
            form.fields['f_pwd'].widget.attrs.update({'readonly': 'readonly'})
        else:
            pts = Posts.objects.filter(id=post_id)
            if len(pts) > 0:
                post = pts[0]
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
                                }
                form = FormPost(default_data)
            else:
                raise ValueError

        for f in ['f_id', 'f_create_tm', 'f_update_tm']:
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

            if f_id == -1:
                post = Posts.objects.create(title=f_title,
                                            subtitle=f_sub_title,
                                            create_time=f_create_tm,
                                            public_time=f_publish_tm,
                                            update_time=f_up_tm,
                                            visit_status=f_visit,
                                            password=f_pwd,
                                            comment_status=f_can_comment,
                                            content=f_content,
                                            author=request.user.id)
                pid = post.id
            else:
                post = Posts.objects.filter(id=f_id).update(title=f_title,
                                                            subtitle=f_sub_title,
                                                            create_time=f_create_tm,
                                                            public_time=f_publish_tm,
                                                            update_time=f_up_tm,
                                                            visit_status=f_visit,
                                                            password=f_pwd,
                                                            comment_status=f_can_comment,
                                                            content=f_content)
                pid = post_id
            return HttpResponseRedirect(reverse('edit_post', kwargs={'post_id': pid}))

    content = {'common': Common.get_commons(request),
               'form': form}

    return render(request, 'management/post_edit.html', content)

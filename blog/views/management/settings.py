from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from blog.views import common
from blog.models import Options


def settings(request):
    # TODO check auth
    content = {'common': common.Common.get_commons(request)}
    print(request.method)
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        try:
            Options.objects.filter(name='blog_name').update(value=request.POST['blog_name'])
            Options.objects.filter(name='blog_desc').update(value=request.POST['blog_desc'])
        except Exception as e:
            print(e)
        return HttpResponseRedirect('/management/settings')
    else:
        pass

    return render(request, 'management/settings.html', content)

from django.http import HttpRequest
from django.shortcuts import render
from blog.models import Options
from blog.views import common


def index(request):
    options = Options.objects.all()
    theme = options.get(name='theme').value
    assert (len(theme) > 0)

    content = {'blog_name': options.get(name='blog_name').value,
               'blog_desc': options.get(name='blog_desc').value,
               'common': common.Common.get_commons(request)}

    return render(request, 'themes/' + theme + '/index.html', content)

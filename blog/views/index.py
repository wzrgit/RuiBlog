from django.http import HttpRequest
from django.shortcuts import render
from blog.models import Options


def index(request):
    options = Options.objects.all()
    theme = options.get(name='theme').value
    assert(len(theme) > 0)

    content = {'blogname': options.get(name='blogname').value,
               'blogdesc': options.get(name='blogdesc').value}

    return render(request, 'themes/' + theme + '/index.html', content)

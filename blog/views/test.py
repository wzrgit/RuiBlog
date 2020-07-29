from django.http import HttpRequest
from django.shortcuts import render
from blog.models import Options
from blog.views import common


def test_base_template(request):
    theme = Options.objects.get(name='theme').value
    assert (len(theme) > 0)
    content = {'common': common.get_commons(request)}
    print(content)
    return render(request, 'themes/' + theme + '/test_template.html', content)

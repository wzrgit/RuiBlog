from django.http import HttpRequest
from blog.models import Options, PostCategory


def get_commons(request):
    options = Options.objects.all()
    common = {'blog_name': options.get(name='blog_name').value,
              'blog_desc': options.get(name='blog_desc').value,
              'categories': PostCategory.objects.values(),
              'is_login': request.user.is_authenticated
              }

    return common

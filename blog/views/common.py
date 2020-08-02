from django.http import HttpRequest
from blog.models import Options, PostCategory


class Common:
    @staticmethod
    def get_commons(request):
        options = Options.objects.all()
        common = {'blog_name': options.get(name='blog_name').value,
                  'blog_desc': options.get(name='blog_desc').value,
                  'categories': PostCategory.objects.values(),
                  'is_login': request.user.is_authenticated
                  }

        return common

    @staticmethod
    def get_response_content(success: object = True):
        if success:
            content = {'status': 'success'}
        else:
            content = {'status': 'error'}

        return content

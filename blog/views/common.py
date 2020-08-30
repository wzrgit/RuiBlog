from django.http import HttpRequest, HttpResponseRedirect, HttpResponseNotFound
from blog.models import Options, PostCategory


class Common:
    @staticmethod
    def get_commons(request):
        options = Options.objects.all()
        common = {'blog_name': options.get(name='blog_name').value,
                  'blog_desc': options.get(name='blog_desc').value,
                  'theme': options.get(name='theme').value,
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
    
    @staticmethod
    def redirect_to_404(request):
        return HttpResponseNotFound()

from blog.models import Options, PostCategory


def GetCommons():
    options = Options.objects.all()
    cates = PostCategory.objects.values()
    common = {'blog_name': options.get(name='blog_name').value,
              'blog_desc': options.get(name='blog_desc').value,
              'categories': cates}

    return common

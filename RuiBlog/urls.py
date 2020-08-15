"""RuiBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blog.views import index as view_index
from blog.views import test as view_test
from blog.views.management import management, settings, posts, albums

urlpatterns = [
    path('/', view_index.index),
    path('index/', view_index.index),
    path('admin/', admin.site.urls),
    path('test/', view_test.test_base_template),
    # management
    path('management/', management.dashboard),
    path('management/dashboard/', management.dashboard),
    path('management/posts/', posts.posts),
    path('management/posts/new/', posts.create_post, name='create_post'),
    path('management/settings/', settings.settings),
    path('management/albums/', albums.albums),
    path('management/create_album/', albums.create_album, name='create_album'),

    # ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


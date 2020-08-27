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
from django.urls import path, include, re_path
from django.conf import settings as dj_settings
from django.conf.urls.static import static
from blog.views import index as view_index
from blog.views import test as view_test
from blog.views import posts as view_posts
from blog.views import album as view_albums
from blog.views.management import management, settings, posts, albums

urlpatterns = [
    path('admin/', admin.site.urls),
    # views
    re_path(r'^$', view_index.index),
    path('index/', view_index.index),
    path('test/', view_test.test_base_template),
    re_path('^posts(/page/(?P<curr_page>\d+))?/$', view_posts.post_list, name='posts_list'),
    path('post/<int:post_id>', view_test.test_base_template, name='post_view'),  # TODO
    path('albums/', view_albums.albums_list , name='albums_list'),
    re_path('^album/(?P<album_id>\d+)(/page/(?P<curr_page>\d+))?/$', view_albums.album_view),  # TODO
    # management
    path('management/', management.dashboard),
    path('management/dashboard/', management.dashboard),
    path('management/posts/', posts.posts),
    path('management/post/edit/', posts.edit_post, name='create_post'),
    re_path(r'^management/post/edit/(?P<post_id>(\-)?\d+)/$', posts.edit_post, name='edit_post'),
    path('management/settings/', settings.settings),
    path('management/albums/', albums.albums),
    path('management/create_album/', albums.create_album, name='create_album'),

    # ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(dj_settings.MEDIA_URL, document_root=dj_settings.MEDIA_ROOT)

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
from django.contrib import admin, auth
from django.urls import path, include, re_path
from django.conf import settings as dj_settings
from django.conf.urls.static import static
from blog.views import index as view_index
from blog.views import test as view_test
from blog.views import posts as view_posts
from blog.views import album as view_albums
from blog.views.management import management, settings as mgr_settings, posts as mgr_posts, albums as mgr_albums

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # views
    re_path(r'^$', view_test.test_base_template, name='home'),  # TODO
    path('index/', view_index.index, name='index'),
    path('test/', view_test.test_base_template),
    re_path('^posts(/page/(?P<curr_page>\d+))?/$', view_posts.post_list, name='posts_list'),
    path('post/<int:post_id>', view_posts.post_view, name='post_view'),
    path('albums/', view_albums.albums_list, name='albums_list'),
    re_path('^album/(?P<album_id>\d+)(/page/(?P<curr_page>\d+))?/$', view_albums.album_view, name='album_view'),
    path('album/upload_img/<int:album_id>', mgr_albums.upload_photo, name='upload_image'),
    path('album/delete_img/', mgr_albums.delete_photo, name='delete_image'),
    path('album/update_img/', mgr_albums.update_photo, name='update_image'),

    # management
    path('management/', management.dashboard),
    path('management/dashboard/', management.dashboard, name='dashboard'),
    path('management/posts/', mgr_posts.posts),
    path('management/post/edit/', mgr_posts.edit_post, name='create_post'),
    re_path(r'^management/post/edit/(?P<post_id>(\-)?\d+)/$', mgr_posts.edit_post, name='edit_post'),
    path('management/posts/remove_to_trash', mgr_posts.remove_post_to_trash, name='remove_post_to_trash'),
    path('management/posts/recover_from_trash', mgr_posts.recover_post_from_trash, name='recover_post_from_trash'),
    path('management/posts/delete', mgr_posts.destroy_post, name='delete_post'),
    path('management/settings/', mgr_settings.settings),
    path('management/albums/', mgr_albums.albums),
    path('management/create_album/', mgr_albums.create_album, name='create_album'),
    path('management/albums/edit/<int:album_id>', mgr_albums.edit_album, name='edit_album'),

    # ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(dj_settings.MEDIA_URL, document_root=dj_settings.MEDIA_ROOT)

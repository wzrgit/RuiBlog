from django.db import models
# from __future__ import unicode_literals


class Options(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=512)
    

class Posts(models.Model):
    VISIT_STATUS = (
        (0, 'draft'),
        (1, 'public'),
        (2, 'protected'),
        (3, 'private')
    )
    
    COMMENT_STATUS = (
        (0, 'closed'),
        (1, 'open')
    )
    
    title = models.CharField(max_length=255, blank=False, null=False)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    author = models.SmallIntegerField(blank=True)
    create_time = models.DateTimeField()
    public_time = models.DateTimeField()
    update_time = models.DateTimeField()
    visit_status = models.SmallIntegerField(default=0, choices=VISIT_STATUS)
    comment_status = models.SmallIntegerField(default=0, choices=COMMENT_STATUS)
    password = models.CharField(max_length=64, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    pin_top = models.BooleanField(default=False)
    remark = models.CharField(max_length=512, blank=True, null=True)


class PostCategory(models.Model):
    name = models.CharField(max_length=64)
    theme = models.CharField(max_length=255, default='default')
    

class CategoryHasPosts(models.Model):
    category = models.ForeignKey(PostCategory, default=1, on_delete=models.SET_DEFAULT)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    

class Album(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=512, blank=True, null=True)
    cover_img = models.CharField(max_length=255, blank=True)
    show_exif = models.BooleanField(default=False)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    remark = models.CharField(max_length=512, blank=True, null=True)
    
    
class Photos(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True)
    alias = models.CharField(max_length=128, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    exif = models.CharField(max_length=512, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)

    


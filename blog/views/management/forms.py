from django import forms
from django.utils.translation import gettext, gettext as _
from django.utils.timezone import now
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField, RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField
from blog.models import Posts


class RuiBlogForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RuiBlogForm, self).__init__(*args, **kwargs)
        for it in iter(self.fields):
            if not isinstance(self.fields[it], (type(forms.BooleanField()), type(forms.ImageField()))):
                self.fields[it].widget.attrs.update({'class': 'form-control'})

    def update_placeholder(self, fields):
        """
        update the placeholder of field to label
        :param fields: list of field names
        :return: 
        """
        for f in fields:
            self.fields[f].widget.attrs.update({'placeholder': self.fields[f].label})


class CreatePost(RuiBlogForm):
    f_title = forms.CharField(label=_('post_title'), max_length=255, required=True)
    f_subtitle = forms.CharField(label=gettext('post_sub_title'), max_length=255)
    f_create_tm = forms.DateTimeField(label=gettext('post_create_time'), initial=now())
    f_public_tm = forms.DateTimeField(label=gettext('post_public_time'), initial=now())
    f_update_tm = forms.DateTimeField(label=gettext('post_update_time'), initial=now())
    f_content = RichTextUploadingFormField()
    f_visit_status = forms.ChoiceField(label=_('post_visit_status'), choices=Posts.VISIT_STATUS)
    f_comment_status = forms.ChoiceField(label=_('post_comment_status'), choices=Posts.COMMENT_STATUS)
    f_pwd = forms.CharField(label=_('post_pwd'), max_length=32)

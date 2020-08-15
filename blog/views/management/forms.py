from django import forms
from django.utils.translation import gettext
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField, RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class RuiBlogForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RuiBlogForm, self).__init__(*args, **kwargs)
        for it in iter(self.fields):
            if not isinstance(self.fields[it], (type(forms.BooleanField()), type(forms.ImageField()))):
                self.fields[it].widget.attrs.update({'class': 'form-control'})


class CreatePost(RuiBlogForm):
    f_title = forms.CharField(label=gettext('post_title'), max_length=255)
    f_subtitle = forms.CharField(label=gettext('post_sub_title'), max_length=255)
    f_create_tm = forms.DateTimeField(label=gettext('post_create_time'))
    f_public_time = forms.DateTimeField(label=gettext('post_public_time'))
    f_update_time = forms.DateTimeField(label=gettext('post_update_time'))
    f_content = RichTextFormField()
    f_visit_status = forms.ChoiceField

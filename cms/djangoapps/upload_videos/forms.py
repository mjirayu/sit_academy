from django import forms

from .models import UploadVideo


def _get_widget(placeholder):
    return forms.TextInput(attrs={'placeholder': placeholder})


class UploadVideoForm(forms.ModelForm):
    video = forms.FileField(label='')

    class Meta:
        model = UploadVideo
        widgets = {
            'name': _get_widget('Enter Filename'),
            'course_id': forms.HiddenInput(),
        }

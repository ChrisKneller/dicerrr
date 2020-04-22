from django import forms
from dice.models import Upload

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('file',)

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs\
            .update({
                'class': 'dropzone'
            })
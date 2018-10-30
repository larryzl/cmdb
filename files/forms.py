from django import forms
from files.models import Files


class UploadFileForm(forms.Form):
    description = forms.CharField(max_length=50)
    file_name = forms.FileField()

class FileListForm(forms.ModelForm):

    class Meta:
        model = Files
        fields = "__all__"
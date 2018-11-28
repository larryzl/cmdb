from django import forms
from files.models import Files


class UploadFileForm(forms.Form):

    description = forms.CharField(
        label='文件描述',
        max_length=50
    )
    file_name = forms.FileField(
        label='选择文件'
    )
    is_shared = forms.BooleanField(
        label='是否共享',
        required=False

    )

class UploadScriptForm(forms.Form):

    description = forms.CharField(
        label='文件描述',
        max_length=50
    )
    file_name = forms.FileField(
        label='选择文件'
    )
    is_shared = forms.BooleanField(
        label='是否共享',
        required=False
    )

class UploadPlaybookForm(forms.Form):

    description = forms.CharField(
        label='文件描述',
        max_length=50
    )
    file_name = forms.FileField(
        label='选择文件'
    )
    is_shared = forms.BooleanField(
        label='是否共享',
        required=False
    )




class FileListForm(forms.ModelForm):

    class Meta:
        model = Files
        fields = "__all__"
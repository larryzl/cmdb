from assets.models import Server,Label,Project,IDC
from django import forms

class ServerFrom(forms.ModelForm):
    ssh_port = forms.CharField(
        label="SSH端口",
        initial="22"
    )
    ssh_user = forms.CharField(
        label="SSH用户名",
        initial="root"
    )
    class Meta:
        model = Server
        fields = ('name','ip','project','label','is_active','system','idc_name','ssh_user','ssh_port','ansible_group')

class ServerEditFrom(forms.ModelForm):
    class Meta:
        model = Server
        fields = "__all__"

class IdcForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = ('name','type','address','contack_name','contack_phone','contack_qq','contack_mail','bandwidth')

class ProjectFrom(forms.ModelForm):
    name = forms.CharField(
        label="名称"
    )
    remark = forms.CharField(
        label="备注"
    )
    class Meta:
        model = Project
        fields = ('name','remark')

class LabelForm(forms.ModelForm):
    name = forms.CharField(
        label="名称"
    )
    remark = forms.CharField(
        label="备注"
    )
    class Meta:
        model = Label
        fields = ('name','remark')

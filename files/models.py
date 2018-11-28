from django.db import models
from users.models import CustomUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import uuid
# Create your models here.


class Files(models.Model):
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    user = models.ForeignKey(CustomUser,verbose_name="用户名",related_name="files_users",to_field='uuid',on_delete=models.CASCADE)
    file_name = models.FileField(upload_to="upload/files/%Y%m%d")
    file_size = models.CharField(max_length=30,verbose_name='文件大小')
    md5 = models.CharField(max_length=30,verbose_name='MD5值')
    description = models.TextField(verbose_name="介绍", blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_shared = models.BooleanField(default=False,verbose_name="是否共享",blank=True)

class AnsibleScript(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    user = models.ForeignKey(CustomUser,related_name='ansible_script_user',to_field='uuid',on_delete=models.CASCADE)
    file_name = models.FileField(upload_to="upload/scripts/%Y%m%d")
    detail = models.TextField(verbose_name='脚本内容')
    file_size = models.CharField(max_length=30,verbose_name='文件大小')
    md5 = models.CharField(max_length=30,verbose_name='MD5值')
    description = models.TextField(verbose_name="介绍", blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_shared = models.BooleanField(default=False,verbose_name="是否共享",blank=True)

    class Meta:
        verbose_name = 'ansible脚本'
        verbose_name_plural = 'ansible脚本'

class AnsiblePlaybook(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    user = models.ForeignKey(CustomUser,related_name='ansible_playbook_user',to_field='uuid',on_delete=models.CASCADE)
    file_name = models.FileField(upload_to="upload/playbooks/%Y%m%d")
    file_size = models.CharField(max_length=30,verbose_name='文件大小')
    md5 = models.CharField(max_length=30,verbose_name='MD5值')
    description = models.TextField(verbose_name="介绍", blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_shared = models.BooleanField(default=False,verbose_name="是否共享",blank=True)

    class Meta:
        verbose_name = 'ansible playbook'
        verbose_name_plural = 'ansible playbook'
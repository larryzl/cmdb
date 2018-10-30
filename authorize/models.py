from django.db import models
# Create your models here.

from users.models import CustomUser
import uuid
from assets.models import Server,Project

class auth_group(models.Model):
    """
    权限组
    """
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    group_name = models.CharField(max_length=100, verbose_name='角色名称', unique=True)
    group_user = models.ManyToManyField(CustomUser, blank=True, verbose_name='所属用户')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    explanation = models.TextField(verbose_name='角色描述')
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = "角色管理"
        verbose_name_plural = verbose_name

class user_auth_cmdb(models.Model):
    """
    cmdb权限
    所有字段全部以0，1来表示
    1表示有此权限，0表示无此权限
    所有数据全部外键关联user表，当用户删除时相应权限也随之删除
    """
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    """
    资产管理
    """
    select_host = models.BooleanField(default=False, verbose_name="查看资产")
    edit_host = models.BooleanField(default=False, verbose_name="修改资产")
    update_host = models.BooleanField(default=False, verbose_name="更新资产")
    add_host = models.BooleanField(default=False, verbose_name="添加主机")
    bat_add_host = models.BooleanField(default=False, verbose_name="批量添加")
    delete_host = models.BooleanField(default=False, verbose_name="删除资产")


    group_name = models.ForeignKey(auth_group, verbose_name='所属角色', help_text="添加角色组权限",on_delete=models.CASCADE)

    def __unicode__(self):
        return self.group_name
        # return "权限管理"

    class Meta:
        verbose_name = "权限管理"
        verbose_name_plural = verbose_name


class AuthSudo(models.Model):
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    groupname = models.CharField(max_length=64, verbose_name="组名", help_text="sudo组")
    shell = models.TextField(verbose_name='命令')
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.groupname

    class Meta:
        managed = True
        db_table = 'AuthSudo'
        verbose_name = "sudo授权"
        verbose_name_plural = verbose_name


class AuthNode(models.Model):
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    user_name = models.ForeignKey(CustomUser, max_length=20, verbose_name="名称", help_text="用户",on_delete=models.CASCADE)
    node = models.ForeignKey(Server, null=True, blank=True, verbose_name='主机', on_delete=models.SET_NULL)
    auth = models.BooleanField(verbose_name='是否管理员', default=0)
    # project = models.CharField(verbose_name='项目名', max_length=128, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user_name

    class Meta:
        managed = True
        db_table = 'AuthNode'
        verbose_name = "主机权限"
        verbose_name_plural = verbose_name

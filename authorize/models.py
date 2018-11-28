from django.db import models
# Create your models here.

from users.models import CustomUser,department_Mode
import uuid
from assets.models import Server,Project

class auth_group(models.Model):
    """
    权限组
    """
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    group_name = models.CharField(max_length=100, verbose_name='角色名称', unique=True)
    group_user = models.ManyToManyField(CustomUser, related_name='user_auth_group',blank=True, verbose_name='所属用户')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    explanation = models.TextField(verbose_name='角色描述')
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = "角色管理"
        verbose_name_plural = verbose_name

# CustomUser.objects.get(email='yantao@tansuotv.com').auth_group_set.all()


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
    idc_list = models.BooleanField(default=False, verbose_name="查看IDC")
    idc_add = models.BooleanField(default=False, verbose_name="添加IDC")
    idc_del = models.BooleanField(default=False, verbose_name="删除IDC")
    idc_edit = models.BooleanField(default=False, verbose_name="修改IDC")
    project_list = models.BooleanField(default=False, verbose_name="查看项目组")
    project_add = models.BooleanField(default=False, verbose_name="添加项目组")
    project_edit = models.BooleanField(default=False, verbose_name="修改项目组")
    project_del = models.BooleanField(default=False, verbose_name="删除项目组")
    label_list = models.BooleanField(default=False, verbose_name="查看标签组")
    label_add = models.BooleanField(default=False, verbose_name="添加标签组")
    label_edit = models.BooleanField(default=False, verbose_name="修改标签组")
    label_del = models.BooleanField(default=False, verbose_name="删除标签组")


    '''
    用户管理
    '''
    user_list = models.BooleanField(default=False, verbose_name="用户管理")
    user_edit = models.BooleanField(default=False, verbose_name="修改用户")
    user_del = models.BooleanField(default=False, verbose_name="删除用户")
    user_active = models.BooleanField(default=False, verbose_name="禁用用户")
    department_list = models.BooleanField(default=False, verbose_name="部门管理")
    department_add = models.BooleanField(default=False, verbose_name="添加部门")
    department_edit = models.BooleanField(default=False, verbose_name="修改部门")
    department_del = models.BooleanField(default=False, verbose_name="删除部门")

    # user_active = models.BooleanField(default=False, verbose_name="禁用用户")
    '''
    权限管理
    '''


    '''
    ansible管理
    '''
    exec_cmd = models.BooleanField(default=False, verbose_name="执行命令")
    update_file = models.BooleanField(default=False, verbose_name="更新文件")


    '''
    文件管理
    '''
    file_list = models.BooleanField(default=False, verbose_name="文件列表")
    upload_file = models.BooleanField(default=False, verbose_name="上传文件")





    group_name = models.ForeignKey(auth_group, related_name='user_auth_cmdb_auth_group',verbose_name='所属角色', help_text="添加角色组权限",on_delete=models.CASCADE)

    def __unicode__(self):
        return self.group_name
        # return "权限管理"

    class Meta:
        verbose_name = "权限管理"
        verbose_name_plural = verbose_name


# user_auth_cmdb.objects.select_related('group_name').filter(group_name__uuid=)

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
    user_name = models.ForeignKey(CustomUser, max_length=20, verbose_name="名称", help_text="用户",on_delete=models.CASCADE,to_field='uuid',related_name='authnode_user')
    node = models.ForeignKey(Server, null=True, blank=True, verbose_name='主机', on_delete=models.CASCADE,to_field='uuid',related_name='authnode_node')
    # auth = models.BooleanField(verbose_name='是否管理员', default=0)
    # project = models.CharField(verbose_name='项目名', max_length=128, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user_name

    class Meta:
        managed = True
        db_table = 'AuthNode'
        verbose_name = "主机权限"
        verbose_name_plural = verbose_name

class AuthGroupNode(models.Model):
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    department_name = models.ForeignKey(department_Mode, max_length=20, verbose_name="名称", help_text="部门",on_delete=models.CASCADE,to_field='uuid',related_name='authdepnode_user')
    node = models.ForeignKey(Server, null=True, blank=True, verbose_name='主机', on_delete=models.CASCADE,to_field='uuid',related_name='authdepnode_node')
    is_active = models.BooleanField(default=True)
    # auth = models.BooleanField(verbose_name='是否管理员', default=0)
    # project = models.CharField(verbose_name='项目名', max_length=128, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)


    class Meta:
        managed = True
        db_table = 'AuthGroupNode'
        verbose_name = "部门权限"
        verbose_name_plural = verbose_name

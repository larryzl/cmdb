from django.db import models
from ansible_api.models import AnsibleServerGroup
import uuid
# Create your models here.

idc_type = (
    (0,"IDC机房"),
    (1,"公有云"),
    (2,"私有云"),
)

server_os = (
    (0,"CentOS 5"),
    (1,"CentOS 6"),
    (2,"CentOS 7"),
    (3,"Ubuntu 16"),
    (4,"Ubuntu 15"),
    (5,"Windows 2012"),
    (6,"Windows 2008"),
)

class IDC(models.Model):
    uuid = models.CharField(primary_key=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    name = models.CharField(max_length=20,verbose_name='机房名称')
    type = models.IntegerField(verbose_name="机房类型",choices=idc_type,blank=True,null=True)

    address = models.CharField(max_length=20,verbose_name='机房位置')
    contack_name = models.CharField(max_length=10,verbose_name='联系人')
    contack_phone = models.CharField(max_length=20,verbose_name='联系电话',blank=True, null=True)
    contack_qq = models.CharField(max_length=10,verbose_name='联系qq',blank=True, null=True)
    contack_mail = models.EmailField(verbose_name='联系邮箱',blank=True, null=True)
    bandwidth = models.CharField(max_length=10,verbose_name='机房带宽',blank=True, null=True)
    class Meta:
        verbose_name = 'IDC列表'
        verbose_name_plural = 'IDC列表'

    def __str__(self):
        return self.name


class Server(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    name = models.CharField(unique=True,max_length=20,verbose_name='主机名')
    ip = models.GenericIPAddressField(unique=True,verbose_name='IP地址')
    project = models.ManyToManyField('Project',blank=True,verbose_name='业务组')
    label = models.ManyToManyField('Label',blank=True,verbose_name='服务标签')
    is_active = models.BooleanField(default=True,verbose_name='使用状态')
    system = models.IntegerField(verbose_name='操作系统',choices=server_os)
    idc_name = models.ForeignKey(IDC,verbose_name='所属机房',on_delete=models.CASCADE)
    location = models.CharField(max_length=30, verbose_name='机架位置',blank=True, null=True)
    check_time = models.DateTimeField(auto_now_add=True,verbose_name="检查时间")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    mod_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")
    ssh_port = models.IntegerField(verbose_name="SSH端口",default=22)
    ssh_user = models.CharField(verbose_name="连接用户名",max_length=20,blank=False,null=False,default="root")
    manufacturer = models.CharField(max_length=20,blank=True, verbose_name='厂商')
    productname = models.CharField(max_length=30,blank=True, verbose_name='产品型号')
    service_tag = models.CharField(max_length=80,blank=True, null=True, verbose_name='序列号')
    cpu_model = models.CharField(max_length=50,blank=True,verbose_name='CPU型号')
    cpu_nums = models.CharField(max_length=50,blank=True,verbose_name='CPU线程数')
    cpu_groups = models.CharField(max_length=50,null=True,blank=True,verbose_name='CPU物理核数')
    mem = models.CharField(max_length=100,blank=True,verbose_name='内存大小')
    disk = models.CharField(max_length=300,blank=True,verbose_name='硬盘大小')
    hostname = models.CharField(max_length=30,blank=True,verbose_name='主机名')
    ip2 = models.CharField(max_length=50,null=True,blank=True, verbose_name='其他IP地址')
    ansible_group = models.ManyToManyField(to=AnsibleServerGroup,blank=True,verbose_name='ansible组')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '主机列表'
        verbose_name_plural = '主机列表'

class AssetOperationLog(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    host = models.ForeignKey("Server",verbose_name="主机ID",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="修改详情",null=True)

    def __str__(self):
        return "资产日志"
    class Meta:
        verbose_name = "资产日志"
        verbose_name_plural = "资产日志"

class Project(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    name = models.CharField(max_length=30,unique=True)
    remark = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '业务组名称'
        verbose_name_plural = '业务组'

class Label(models.Model):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    name = models.CharField(max_length=30,unique=True)
    remark = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '服务标签'
        verbose_name_plural = '服务标签'
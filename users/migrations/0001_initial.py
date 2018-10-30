# Generated by Django 2.0.5 on 2018-10-26 08:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='用户名')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('mobile', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+()-]+$', 'Enter a valid mobile number.', 'invalid')], verbose_name='手机')),
                ('session_key', models.CharField(blank=True, max_length=60, null=True, verbose_name='session_key')),
                ('user_key', models.TextField(blank=True, null=True, verbose_name='用户登录key')),
                ('menu_status', models.BooleanField(default=False, verbose_name='用户菜单状态')),
                ('user_active', models.BooleanField(default=0, verbose_name='设置密码状态')),
                ('uuid', models.CharField(default=uuid.UUID('a75bd0e3-25f1-39f5-b06a-12453ac72cac'), max_length=64)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
        ),
        migrations.CreateModel(
            name='department_Mode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='部门名称')),
                ('description', models.TextField(blank=True, null=True, verbose_name='介绍')),
                ('desc_gid', models.IntegerField(blank=True, choices=[(1001, '运维部'), (1002, '架构部'), (1003, '研发部'), (1004, '测试部')], null=True, verbose_name='部门组')),
            ],
            options={
                'verbose_name_plural': '部门',
                'verbose_name': '部门',
            },
        ),
        migrations.CreateModel(
            name='DepartmentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_groups_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='组名')),
                ('description', models.TextField(blank=True, null=True, verbose_name='介绍')),
            ],
            options={
                'verbose_name_plural': '部门组',
                'verbose_name': '部门组',
            },
        ),
        migrations.CreateModel(
            name='server_auth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='服务器')),
                ('user_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='用户名')),
                ('first_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='姓名')),
                ('auth_weights', models.BooleanField(default=0, verbose_name='权限')),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '日志记录',
                'verbose_name': '日志记录',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.department_Mode', verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]

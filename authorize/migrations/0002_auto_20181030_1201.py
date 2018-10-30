# Generated by Django 2.0.5 on 2018-10-30 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorize', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='add_department',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='add_idc',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='add_line_auth',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='add_project',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='add_user',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='auth_highstate',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='auth_log',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='auth_project',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='cmdb_log',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='del_idc',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='delete_project',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='delete_user',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='edit_idc',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='edit_pass',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='edit_project',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='edit_user',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='project_auth',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='salt_keys',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='select_idc',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='server_audit',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='setup_system',
        ),
        migrations.RemoveField(
            model_name='user_auth_cmdb',
            name='upload_system',
        ),
    ]

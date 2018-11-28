from django.urls import path,re_path

from ansible_api import views


urlpatterns = [
    re_path(r'^ansible/command$',views.exec_cmd,name='ansible_cmd'),
    # re_path('^ansible/$', views.index,name='ansible_index'),
    # re_path(r'^ansible/files$',views.update_file,name='ansible_update_file'),
    re_path(r'^ansible/playbook/view$',views.playbookView,name='playbook_view'),

    re_path('^log', views.ansible_log,name='job_log'),

]


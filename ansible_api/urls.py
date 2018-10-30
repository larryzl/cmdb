from django.urls import path,re_path

from ansible_api import views


urlpatterns = [
    re_path('^ansible/$', views.index,name='ansible_index'),
    re_path(r'^ansible/command$',views.exec_cmd,name='ansible_cmd'),

    re_path('^cronjob', views.index,name='cron_job'),
    re_path('^log', views.index,name='job_log'),

]


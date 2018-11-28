from django.urls import path,re_path

from files import views


urlpatterns = [
    re_path(r'list/$',views.file_list,name='file_list'),
    re_path('^list/upload/$', views.upload_file,name='upload'),
    re_path('^scripts/$', views.scripts_list,name='scripts'),
    re_path('^scripts/upload/$',views.upload_script,name='script_upload'),
    re_path('^download/', views.upload_file,name='download'),
    re_path('^playbook/$', views.playbook_list,name='playbook'),
    re_path('^playbook/upload/$', views.upload_playbook,name='playbook_upload'),

]




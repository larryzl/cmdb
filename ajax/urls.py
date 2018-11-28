from django.urls import path,re_path

from ajax import views


urlpatterns = [
    re_path(r'^server/list', views.getServerList,name='ajax_server_list'),
    re_path(r'^server/select',views.displayServerList,name='ajax_server_select'),
    re_path(r'^server/update',views.server_update,name='server_update'),
    re_path(r'^file/detail',views.file_detail,name='ajax_get_file_detail'),
    re_path(r'^ansible/run$',views.ajax_ansible_cmd,name='ajax_ansible_cmd'),
    re_path(r'^playbook/review$',views.reViewPlaybook,name='ajax_review_playbook')

]


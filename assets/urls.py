from django.urls import path,re_path

from assets import views


urlpatterns = [
    re_path('^server/list', views.server_list,name='server_list'),
    re_path('^server/add$',views.server_add,name='server_add'),
    re_path('^server/edit/(?P<id>[\w|\-]+)/',views.server_edit,name='server_edit'),
    re_path('^server/change/status/',views.server_change_status,name='server_change_status'),
    re_path('^server/del/',views.server_del,name='server_del'),
    re_path(r'^server/detail/(?P<id>[\w|\-]+)/',views.server_edit,name='server_detail'),
    re_path(r'^server/add/batch',views.server_add_batch,name='server_add_batch'),

    re_path(r'^idc/list',views.idc_list,name='idc_list'),
    re_path(r'^idc/add',views.idc_add,name='idc_add'),
    re_path(r'^idc/del/',views.idc_del,name='idc_del'),
    re_path(r'^idc/edit/(?P<id>[\w|\-]+)/$',views.idc_edit,name='idc_edit'),

    re_path(r'^project/list',views.project_list,name='project_list'),
    re_path(r'^project/add',views.project_add,name='project_add'),
    re_path(r'^project/add',views.project_add,name='project_del'),
    re_path(r'^project/edit/(?P<id>[\w|\-]+)/$',views.project_edit,name='project_edit'),

    re_path(r'^lable/list',views.label_list,name='lable_list'),
    re_path(r'^lable/add',views.lable_add,name='lable_add'),
    re_path(r'^lable/edit/(?P<id>[\w|\-]+)/$',views.lable_edit,name='lable_edit'),

]


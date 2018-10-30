from django.urls import path,re_path

from authorize import views


urlpatterns = [
    re_path('^auth-group/list', views.auth_index,name='auth_list'),
    re_path('^auth-group/add', views.auth_add,name='auth-group_add'),
    re_path('^auth-group/edit/(?P<id>[\w|\-]+)/', views.auth_edit,name='auth-group_edit'),
    re_path('^auth-group/del/', views.auth_del,name='auth-group_del'),
    re_path('^auth-group/authorize/(?P<id>[\w|\-]+)/',views.auth_group_authorize,name='auth-group_authorize')




]


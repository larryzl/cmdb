from django.urls import path,re_path

from ajax import views


urlpatterns = [
    re_path('^server/list', views.getServerList,name='ajax_server_list'),
    re_path(r'^server/update',views.server_update,name='server_update'),
]


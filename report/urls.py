from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.report_list, name = 'report_list'),
    url(r'^create', views.create_report, name = 'create_report'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail_report, name = 'detail_report'),
    url(r'^(?P<pk>[0-9]+)/stage1/$', views.page_stage1, name = 'page_stage1'),
    url(r'^(?P<pk>[0-9]+)/stage2/$', views.page_stage2, name = 'page_stage2'),
    url(r'^(?P<pk>[0-9]+)/stage3/$', views.page_stage3, name = 'page_stage3'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.edit_report, name = 'edit_report'),
    url(r'^(?P<report_id>[0-9]+)/delete/(?P<item_id>[0-9]+)/$', views.delete_item, name = 'delete_item'),
    url(r'^(?P<report_id>[0-9]+)/add/$', views.add_item, name = 'add_item'),
    url(r'^logout/$', 'django.contrib.auth.views.logout')

]

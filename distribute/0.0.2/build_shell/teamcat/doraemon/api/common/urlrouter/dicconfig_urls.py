#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.common.views import dic_config_view


api_dicconfig_router =[
    url(r"dicconfig/(?P<type_id>.+)/dicconfigs$",dic_config_view.DicConfigListView.as_view()),
    url(r"dicconfig/(?P<type_id>.+)/(?P<value>.+)$",dic_config_view.DicConfigView.as_view()),
                  ]

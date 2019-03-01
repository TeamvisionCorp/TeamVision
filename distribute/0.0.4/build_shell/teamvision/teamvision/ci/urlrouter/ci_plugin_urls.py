#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.ci.views.ci_plugin_view import get_plugin


plugin_router =[url(r"plugin/(\d{1,9})/get_plugin",get_plugin),
                ]

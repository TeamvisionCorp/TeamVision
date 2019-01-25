#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views import project_common_view

common_router=[url(r"^os/(\d{1,6})/os_version_controll$",project_common_view.os_version_dropdownlist),
               url(r"^os/(\d{1,6})/os_version_menu$",project_common_view.os_version_menu),
                 ]
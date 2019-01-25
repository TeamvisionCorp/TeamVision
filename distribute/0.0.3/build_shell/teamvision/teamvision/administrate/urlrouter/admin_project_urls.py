#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from teamvision.administrate.views import admin_project_view

admin_project_router=[
                    url(r"project/all$",admin_project_view.project_list),
                 ]
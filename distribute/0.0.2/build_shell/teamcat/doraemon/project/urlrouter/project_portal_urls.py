#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views.portal_view import all,project_filter

portal_router=[
               url(r'^$',all),
               url(r"portal/all$",all),
               url(r"portal/filter$",project_filter),
               url(r"product/(\d{1,9})/project$",all)]
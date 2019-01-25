#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.home.views.home_project_view import all

project_router=[url(r"project/(all)",all),
                url(r"product/(\d{1,9})/project",all)]
#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.home.views.home_device_view import all,device_filter,borrow_device

device_router=[url(r"device/all$",all),
               url(r"device/filter$",device_filter),
               url(r"device/borrow$",borrow_device),
            ]
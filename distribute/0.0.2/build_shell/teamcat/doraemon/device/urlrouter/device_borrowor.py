#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.device.views.device_view import all,device_filter,borrow_device

device_borrow_router=[url(r"all$",all),
               url(r"filter$",device_filter),
               url(r"borrow$",borrow_device),
            ]
#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.interface.views import dashboard_view

dashboard_router=[url(r"(\d{1,9})/dashboard$",dashboard_view.index),
               ]
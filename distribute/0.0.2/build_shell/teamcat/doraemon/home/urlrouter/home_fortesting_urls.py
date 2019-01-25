#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.home.views.home_fortesting_view import all

fortesting_router=[url(r"fortesting/(all)",all)]
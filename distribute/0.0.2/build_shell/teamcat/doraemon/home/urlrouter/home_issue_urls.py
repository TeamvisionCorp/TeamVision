#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.home.views.home_issue_view import all

issue_router=[url(r"issue/(\d{1,9})",all)]
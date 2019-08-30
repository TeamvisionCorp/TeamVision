#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.home.views.home_page_view import home_page,project_summary,projects_json,device_summary

un_login_router=[url(r'^$',home_page),
             url(r'^project_summary$',project_summary),
             url(r'^project_json$',projects_json),
             url(r'^device$',device_summary),
             
             ]
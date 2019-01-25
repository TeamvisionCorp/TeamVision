#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views import project_statistics_view

statistics_router=[url(r"^(\d{1,6})/statistics/([a-zA-Z]*$)",project_statistics_view.index),
                   url(r"^(\d{1,6})/version/(\d{1,6})/statistics/issue_count_status",project_statistics_view.issue_count_bystatus),
             ]
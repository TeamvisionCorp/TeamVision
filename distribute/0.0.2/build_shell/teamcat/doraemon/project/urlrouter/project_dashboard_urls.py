#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views.project_dashboard_view import index_list,more_activites

dashboard_router=[url(r"(\d{1,6})/dashboard/$",index_list),
                  url(r"(\d{1,6})/dashboard/more_activites",more_activites)]
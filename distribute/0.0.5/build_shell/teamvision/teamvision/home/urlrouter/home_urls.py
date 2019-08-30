#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.home.urlrouter.home_dashboard_urls import dashboard_router
from teamvision.home.urlrouter.home_project_urls import project_router
# from doraemon.home.urlrouter.home_autotask_urls import autotask_router
from teamvision.home.urlrouter.home_fortesting_urls import fortesting_router
from teamvision.home.urlrouter.home_task_urls import task_router
from teamvision.home.urlrouter.home_webapps_urls import webapps_router
from teamvision.home.urlrouter.home_device_urls import device_router
from teamvision.home.urlrouter.home_issue_urls import issue_router
from teamvision.home.urlrouter.home_page_urls import un_login_router


urlpatterns =dashboard_router+fortesting_router+task_router+webapps_router+device_router+project_router+issue_router

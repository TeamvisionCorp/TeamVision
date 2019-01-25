#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.conf.urls import url
from doraemon.project.urlrouter.project_dashboard_urls import dashboard_router
from doraemon.project.urlrouter.project_task_urls import task_router
from doraemon.project.urlrouter.project_settings_urls import settings_router
from doraemon.project.urlrouter.project_fortesting_urls import fortesting_router
from doraemon.project.urlrouter.project_version_urls import  version_router
from doraemon.project.urlrouter.project_member_urls import member_router
from doraemon.project.urlrouter.project_webhook_urls import webhook_router
from doraemon.project.urlrouter.project_portal_urls import portal_router
from doraemon.project.urlrouter.project_archive_urls import archive_router
from doraemon.project.urlrouter.project_issue_urls import issue_router
from doraemon.project.urlrouter.project_common_urls import common_router
from doraemon.project.urlrouter.project_statistics_urls import statistics_router



urlpatterns =portal_router+dashboard_router+task_router+settings_router+fortesting_router
urlpatterns=urlpatterns+version_router+member_router+webhook_router+archive_router+issue_router+common_router
urlpatterns=urlpatterns+statistics_router
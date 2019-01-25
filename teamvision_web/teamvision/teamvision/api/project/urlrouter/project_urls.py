# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.api.project.urlrouter.project_fortesting_urls import api_fortesting_router
from teamvision.api.project.urlrouter.project_member_urls import api_member_router
from teamvision.api.project.urlrouter.project_module_urls import api_module_router
from teamvision.api.project.urlrouter.project_version_urls import api_version_router
from teamvision.api.project.urlrouter.project_issue_statistics_urls import api_statistics_router
from teamvision.api.project.urlrouter.project_issue_urls import api_issue_router
from teamvision.api.project.urlrouter.project_task_urls import api_task_router
from teamvision.api.project.urlrouter.project_report_urls import api_report_router
from teamvision.api.project.urlrouter.project_task_statistics_urls import api_task_statistics_router

urlpatterns = api_fortesting_router + api_version_router + api_member_router + api_statistics_router + api_issue_router
urlpatterns = urlpatterns + api_task_router+api_module_router+api_report_router+api_task_statistics_router

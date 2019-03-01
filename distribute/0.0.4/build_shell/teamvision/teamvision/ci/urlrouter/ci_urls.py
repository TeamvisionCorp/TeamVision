#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.ci.urlrouter.ci_dashboard_urls import dashboard_router
from teamvision.ci.urlrouter.ci_deploy_urls import deploy_router
from teamvision.ci.urlrouter.ci_task_urls import task_router
from teamvision.ci.urlrouter.ci_build_urls import build_router
from teamvision.ci.urlrouter.ci_plugin_urls import plugin_router
from teamvision.ci.urlrouter.ci_service_urls import service_router
from teamvision.ci.urlrouter.ci_settings_urls import settings_router
from teamvision.ci.urlrouter.ci_task_parameter_urls import task_parameter_router
from teamvision.ci.urlrouter.ci_history_urls import history_router
from teamvision.ci.urlrouter.ci_testing_urls import testing_router


urlpatterns =dashboard_router+deploy_router+build_router+task_router+plugin_router+service_router+settings_router
urlpatterns=urlpatterns+task_parameter_router+history_router+testing_router
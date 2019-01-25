#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.api.ci.urlrouter import ci_task_urls
from teamvision.api.ci.urlrouter.ci_agent_urls import api_agent_router
from teamvision.api.ci.urlrouter.ci_service_urls import deploy_service_router
from teamvision.api.ci.urlrouter.ci_server_urls import deploy_server_router
from teamvision.api.ci.urlrouter.ci_crendentials_urls import ci_crendentials_router
from teamvision.api.ci.urlrouter.ci_task_plugin_urls import task_plugin_router
from teamvision.api.ci.urlrouter.auto_testing_urls import auto_testing_result_router
from teamvision.api.ci.urlrouter.case_tag_urls import case_tag_router
from teamvision.api.ci.urlrouter.ci_task_basic_urls import ci_task_basic_router
from teamvision.api.ci.urlrouter.ci_task_flow_urls import ci_task_flow_router
from teamvision.api.ci.urlrouter.ci_task_log_urls import ci_task_log_router
from teamvision.api.ci.urlrouter.ci_flow_history_urls import ci_flow_history_router







urlpatterns =ci_task_urls.api_task_router+ci_task_urls.task_history_router+ci_task_urls.api_task_router
urlpatterns=urlpatterns+api_agent_router+deploy_service_router+ci_task_log_router
urlpatterns=urlpatterns+deploy_server_router+ci_crendentials_router
urlpatterns=urlpatterns+task_plugin_router+auto_testing_result_router+case_tag_router+ci_task_basic_router
urlpatterns=urlpatterns+ci_task_flow_router+ci_flow_history_router

#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.common.urlrouter.agent_urls import api_agent_router
from doraemon.api.common.urlrouter.user_urls import api_user_router
from doraemon.api.common.urlrouter.task_queue_urls import api_task_queue_router
from doraemon.api.common.urlrouter.file_info_urls import api_file_router
from doraemon.api.common.urlrouter.simple_mq_urls import api_simplemq_router
from doraemon.api.common.urlrouter.dicconfig_urls import api_dicconfig_router



urlpatterns =api_agent_router+api_task_queue_router+api_file_router+api_simplemq_router+api_dicconfig_router
urlpatterns = urlpatterns+api_user_router
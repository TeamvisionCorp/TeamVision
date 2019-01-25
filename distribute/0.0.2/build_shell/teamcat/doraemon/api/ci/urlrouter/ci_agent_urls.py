#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.ci.views.ci_agent_view import get_agent,update_agent_status


api_agent_router=[url(r"agent/get_agent",get_agent),
                  url(r"agent/update_agent_status",update_agent_status),
             ]

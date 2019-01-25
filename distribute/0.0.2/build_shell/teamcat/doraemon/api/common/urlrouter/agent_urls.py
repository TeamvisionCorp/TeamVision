#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.common.views import agent_view


api_agent_router =[url(r"agent/(?P<id>.+)",agent_view.AgentView.as_view()),
                  url(r"agents$",agent_view.AgentListView.as_view()),
                  ]

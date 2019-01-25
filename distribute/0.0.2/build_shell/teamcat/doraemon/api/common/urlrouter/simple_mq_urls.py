#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.common.views import simple_mq_view


api_simplemq_router =[url(r"simple_mq$",simple_mq_view.SimpleMQView.as_view()),
#                   url(r"agents$",agent_view.AgentListView.as_view()),
                  ]

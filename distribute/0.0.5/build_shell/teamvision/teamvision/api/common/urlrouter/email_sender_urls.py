#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.common.views import send_email_view


api_emailsend_router =[url(r"send_email$",send_email_view.EmailSendView.as_view()),
#                   url(r"agents$",agent_view.AgentListView.as_view()),
                  ]

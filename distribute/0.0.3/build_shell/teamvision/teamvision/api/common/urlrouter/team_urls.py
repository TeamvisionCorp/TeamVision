#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.common.views import team_view


api_team_router =[url(r"team/(?P<id>.+)$",team_view.TeamView.as_view()),
                  url(r"teams/my$",team_view.TeamListView.as_view()),
                  ]

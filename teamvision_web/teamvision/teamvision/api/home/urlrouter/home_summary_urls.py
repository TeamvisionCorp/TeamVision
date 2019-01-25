#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.home.views import home_summary_view



api_home_summary_router=[url(r"todo/summary$",home_summary_view.TodoSummaryView.as_view()),
                         url(r"activity/list$",home_summary_view.ActivityListView.as_view()),

                         ]


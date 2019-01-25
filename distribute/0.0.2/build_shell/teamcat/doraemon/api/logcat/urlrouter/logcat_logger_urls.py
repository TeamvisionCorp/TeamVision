#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.api.logcat.views import logcat_logger_view



api_logger_router=[url(r"logger/(?P<id>.+)/$",logcat_logger_view.LoggerView.as_view()),
                         url(r"loggers/$",logcat_logger_view.LoggerListView.as_view()),
                         url(r"logger/$",logcat_logger_view.LoggerCreateView.as_view()),
                         ]


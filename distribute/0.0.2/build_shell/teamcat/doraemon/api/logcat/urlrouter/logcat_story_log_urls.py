#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.api.logcat.views import logcat_business_log_view



api_storylog_router=[url(r"businesslog/(?P<device_id>.+)/$",logcat_business_log_view.BusinessLogListView.as_view()),
                        url(r"businesslog/$",logcat_business_log_view.BusinessLogCreateView.as_view()),
                         ]


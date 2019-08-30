#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.logcat.views import logger_view

logcat_home_router=[url(r"logger$",logger_view.all),
                    url(r"logger/more_bslog$",logger_view.more_business_log),
                    url(r"logger/(\d{1,9})/delete$",logger_view.remove_logger),
                    url(r"logger/logger_list$",logger_view.get_logger_list),
            ]
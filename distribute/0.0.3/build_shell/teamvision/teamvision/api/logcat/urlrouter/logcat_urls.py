#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from teamvision.api.logcat.urlrouter.logcat_logger_urls import api_logger_router
from teamvision.api.logcat.urlrouter.logcat_story_log_urls import api_storylog_router



urlpatterns =api_logger_router+api_storylog_router

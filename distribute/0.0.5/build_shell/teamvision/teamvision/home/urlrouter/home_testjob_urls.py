#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from teamvision.home.views.home_testjob_view import index_list
from teamvision.home.views.home_testjob_view import load_leftnavigater
from teamvision.home.views.home_testjob_view import load_testjob_list,load_content_activity,load_left_sub_navigater




urlpatterns = patterns(
                       r"testjob",
                       url(r"index",index_list),
                       url(r"get_left_navigater",load_leftnavigater),
                       url(r"get_left_sub_nav",load_left_sub_navigater),
                       url(r"get_testjob_view",load_content_activity),
                       url(r"get_testjob_list",load_testjob_list)
                       
                       )

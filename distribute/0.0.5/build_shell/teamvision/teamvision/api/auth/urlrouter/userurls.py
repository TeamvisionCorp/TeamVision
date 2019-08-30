#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.api.auth.views import userview


api_user_router =[url(r"user/(?P<id>.+)",userview.UserView.as_view()),
                  url(r"users$",userview.UserListView.as_view()),
                  ]

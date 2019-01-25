#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.common.views import user_view


api_user_router =[url(r"user/(?P<id>.+)/",user_view.UserView.as_view()),
                  url(r"users/list",user_view.UserListView().as_view())
                  ]

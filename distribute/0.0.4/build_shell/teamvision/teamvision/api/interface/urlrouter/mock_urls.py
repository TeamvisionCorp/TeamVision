#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.interface.views import mock_api_view,mock_response_view


api_mock_router =[url(r"mock/api/(?P<id>.+)",mock_api_view.MockApiView.as_view()),
                  url(r"mock/apis$",mock_api_view.MockApiListView.as_view()),
                  url(r"mock/api_tree$",mock_api_view.MockApiTreeView.as_view()),
                  url(r"mock/response/(?P<id>.+)",mock_response_view.MockResponseView.as_view()),
                  url(r"mock/responses$",mock_response_view.MockResponseListView.as_view()),
                  ]

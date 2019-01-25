#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.ci.views import case_tag_view


case_tag_router=[url(r"case_tag/(?P<id>.+)/$",case_tag_view.CaseTagView.as_view()),
                 url(r"case_tags",case_tag_view.CaseTagListView.as_view()),
                 ]
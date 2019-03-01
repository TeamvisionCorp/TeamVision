#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.common.views import file_archive_view


api_file_router =[url(r"file/(?P<file_id>.+)",file_archive_view.FileArchiveView.as_view()),
                  ]

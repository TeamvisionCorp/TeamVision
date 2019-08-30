#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.project.views import project_document_view



api_document_router=[url(r"document/(?P<document_id>.+)/$",project_document_view.ProjectDocumentView.as_view()),
                     url(r"(?P<project_id>.+)/documents/$",project_document_view.ProjectDocumentListView.as_view()),
                     url(r"document/upload_document$",project_document_view.ProjectDocumentUploadView.as_view()),
                     url(r"document/(?P<file_id>.+)/download_document$",project_document_view.ProjectDocumentUploadView.as_view()),
                         ]


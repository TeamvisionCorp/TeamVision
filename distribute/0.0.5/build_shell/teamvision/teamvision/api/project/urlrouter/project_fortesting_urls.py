#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.project.views import project_fortesting_view



api_fortesting_router=[
              url(r"fortesting/(?P<fortesting_id>.+)/$", project_fortesting_view.ProjectFortestingView.as_view()),
              url(r"fortesting/(?P<fortesting_id>.+)/update_status", project_fortesting_view.ProjectFortestingUpdateStatusView.as_view()),
              url(r"fortesting/upload_files", project_fortesting_view.ProjectFortestingAttachementView.as_view()),
              url(r"fortesting/delete_file/(?P<file_id>.+)", project_fortesting_view.ProjectFortestingAttachementView.as_view()),
              url(r"fortesting/download_file/(?P<file_id>.+)", project_fortesting_view.ProjectFortestingAttachementView.as_view()),
              url(r"(?P<project_id>.+)/version/(?P<version_id>.+)/fortestings$", project_fortesting_view.ProjectFortestingListView.as_view()),
             ]

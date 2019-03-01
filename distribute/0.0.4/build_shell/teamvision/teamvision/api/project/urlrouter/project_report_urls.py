# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.project.views import project_report_view

api_report_router = [
    url(r"report/bvt", project_report_view.ProjectBVTReportListView.as_view()),
    url(r"report/bvt/(?P<id>\w{24,24})", project_report_view.ProjectBVTReportView.as_view()),
    url(r"report/testprogress$", project_report_view.ProjectTestProgressReportListView.as_view()),
    url(r"fortesting/(?P<fortesting_id>.+)/(?P<report_type>.+)$", project_report_view.FortestingTestProgressReportView.as_view()),
    url(r"report/testprogress/(?P<id>\w{24,24})", project_report_view.ProjectTestProgressReportView.as_view()),
    url(r"report/testcomplete$", project_report_view.ProjectTestCompleteReportListView.as_view()),
    url(r"report/testcomplete/(?P<id>\w{24,24})", project_report_view.ProjectTestCompleteReportView.as_view()),
]

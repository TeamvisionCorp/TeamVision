#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.project.views import project_issue_view



api_issue_router=[url(r"(?P<project_id>[\d]+)/version/(?P<version_id>[\d]+)/issues$",project_issue_view.IssueListView.as_view()),
                        url(r"issue/(?P<issue_id>[\d]+)$",project_issue_view.IssueView.as_view()),
                         url(r"issue/status$",project_issue_view.IssueStatusList.as_view()),
                         url(r"issue/severities",project_issue_view.IssueSeverityList.as_view()),
                         url(r"issue/resolve_results",project_issue_view.IssueResolveResultList.as_view()),
                         url(r"issue/project_phrase",project_issue_view.IssueProjectPhraseList.as_view()),
                         url(r"issue/categories",project_issue_view.IssueCategoryList.as_view()),
                         url(r"issue/priority",project_issue_view.IssuePriorityList.as_view()),
                         url(r"issue/os",project_issue_view.ProjectOSList.as_view()),
                         url(r"issue/attachments", project_issue_view.ProjectIssueAttachementListView.as_view()),
                         url(r"issue/(?P<issue_id>.+)/attachment/(?P<file_id>.+)", project_issue_view.ProjectIssueAttachementView.as_view()),
                         url(r"(?P<project_id>.+)/project_modules$",project_issue_view.ProjectModuleList.as_view()),
                         url(r"(?P<project_id>.+)/issue/export$",project_issue_view.ProjectIssueExportView.as_view()),
                         url(r"issue/(?P<issue_id>.+)/activities$",project_issue_view.IssueActivityList.as_view()),
                         ]


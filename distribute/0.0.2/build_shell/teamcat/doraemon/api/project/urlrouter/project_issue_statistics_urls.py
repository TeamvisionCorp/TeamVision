#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from doraemon.api.project.views import issue_statistics_view



api_statistics_router=[url(r"(?P<project_id>.+)/(?P<version_id>.+)/statistics/issue_trend_new$",issue_statistics_view.IssueTrendNew.as_view()),
                       url(r"(?P<project_id>.+)/(?P<version_id>.+)/statistics/issue_trend_total$",issue_statistics_view.IssueTrendTotal.as_view()),
                       url(r"(?P<project_id>.+)/statistics/version_total_issue$",issue_statistics_view.IssueTotalByVersion.as_view()),
                       url(r"(?P<project_id>.+)/(?P<version_id>.+)/statistics/unclosed_issue",issue_statistics_view.UnclosedIssueByPeople.as_view()),
                       url(r"(?P<project_id>.+)/(?P<version_id>.+)/statistics/issue_count_per_module",issue_statistics_view.IssueCountPerModule.as_view()),
                       url(r"(?P<project_id>.+)/(?P<version_id>.+)/statistics/issue_count_by_severity$",issue_statistics_view.IssueCountBySeverity.as_view()),
                       url(r"(?P<project_id>.+)/(?P<version_id>.+)/statistics/issue_count_by_category$",issue_statistics_view.IssueCountByCategory.as_view()),
                       url(r"(?P<project_id>.+)/(?P<version_id>.+)/statistics/issue_count_by_resolveresult",issue_statistics_view.IssueCountByResolveResult.as_view()),
                       url(r"issue/daily_statistics$",issue_statistics_view.IssueDailyStatisticsListView.as_view()),
                       url(r"issue/version_statistics$",issue_statistics_view.IssueVersionStatisticsListView.as_view()),
                        url(r"issue/daily_statistics/(?P<id>.+)$",issue_statistics_view.IssueDailyStatisticsView.as_view()),
                       url(r"issue/version_statistics/(?P<id>.+)$",issue_statistics_view.IssueVersionStatisticsView.as_view()),
                         ]


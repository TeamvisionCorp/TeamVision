#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views import auto_testing_result_view,auto_case_result_view,auto_case_view
from teamvision.api.ci.views import service_host_view


auto_testing_result_router=[url(r"auto_testing_result/(?P<id>.+)/$",auto_testing_result_view.AutoTestingResultView.as_view()),
                         url(r"auto_testing_results$",auto_testing_result_view.AutoTestingResultListView.as_view()),
                         url(r"auto_case_result/(?P<id>.+)/$",auto_case_result_view.AutoTestingCaseResultView.as_view()),
                         url(r"auto_case_results$",auto_case_result_view.AutoTestingCaseResultListView.as_view()),
                         
                          url(r"auto_unittest_result/(?P<id>.+)/$",auto_case_result_view.UnitTestCaseResultView.as_view()),
                         url(r"auto_unittest_results$",auto_case_result_view.UnitTestCaseResultListView.as_view()),
                         
                         url(r"auto_case/(?P<id>.+)/$",auto_case_view.AutoCaseView.as_view()),
                         url(r"auto_cases$",auto_case_view.AutoCaseListView.as_view()),
                
                         
                         url(r"service_host/(?P<id>.+)/$",service_host_view.ServiceHostView.as_view()),
                         url(r"service_hosts",service_host_view.ServiceHostListView.as_view()),
                         
                         
                         ]

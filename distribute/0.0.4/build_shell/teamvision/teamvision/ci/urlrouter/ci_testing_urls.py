#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.ci.views import ci_testing_view
from teamvision.ci.views.ci_task_view import start_task




testing_router =[url(r"testing/(all)",ci_testing_view.index_list),
                url(r"testing/product/(\d{1,9})$",ci_testing_view.index_list),
                url(r"testing/(\d{1,9})/(history)$",ci_testing_view.run_result),
                url(r"testing/(\d{1,9})/(config)$",ci_testing_view.config_task),
                url(r"testing/(\d{1,9})/(parameter)$",ci_testing_view.task_parameter),
                url(r"testing/(\d{1,9})/(testing)$",ci_testing_view.build_with_parameter_page),
                url(r"testing/(\d{1,9})/history/(testing_clean)/",ci_testing_view.history_clean),
                url(r"testing/result/(\d{1,9})/analytics",ci_testing_view.result_analytics),
                url(r"testing/result/(\d{1,9})/caseresult/(\d{1,2})",ci_testing_view.result_detail),
                url(r"testing/caseresult/(\d{1,9})/stace_track",ci_testing_view.case_result_stace_track),
                url(r"testing/(\d{1,9})/start$",start_task),
                url(r"testing/(\d{1,9})/caseresult/export",ci_testing_view.export_case_result),
                ]

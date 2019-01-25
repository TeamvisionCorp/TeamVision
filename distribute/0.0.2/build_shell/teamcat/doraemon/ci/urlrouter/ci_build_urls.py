#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.ci.views import ci_build_view
from doraemon.ci.views.ci_task_view import start_task




build_router =[url(r"build/(all)",ci_build_view.index_list),
                url(r"build/product/(\d{1,9})$",ci_build_view.index_list),
                url(r"build/(\d{1,9})/(history)$",ci_build_view.task_history),
                url(r"build/(\d{1,9})/(unittest_history)$",ci_build_view.unittest_history),
                url(r"build/(\d{1,9})/(config)$",ci_build_view.config_task),
                url(r"build/(\d{1,9})/(parameter)$",ci_build_view.task_parameter),
                url(r"build/(\d{1,9})/(build)$",ci_build_view.build_with_parameter_page),
                url(r"build/(\d{1,9})/(changelog)$",ci_build_view.task_changelog),
                url(r"build/(\d{1,9})/history/(build_clean)/",ci_build_view.history_clean),
                url(r"build/(\d{1,9})/start$",start_task),
                ]

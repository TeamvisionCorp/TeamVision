#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.ci.views import ci_task_basic_view
from teamvision.api.common.views.task_queue_view import  TaskQueueDoneView
from teamvision.api.ci.views import ci_task_history_view
from teamvision.api.ci.views import ci_task_parameter_view
from teamvision.api.ci.views import citask_trigger_view
from teamvision.api.ci.views import ci_task_stage_view

ci_task_basic_router=[url(r"task/(?P<id>.+)/(?P<operation>.+)/$",ci_task_basic_view.CITaskOperationView.as_view()),
                 url(r"task/(?P<id>.+)/$",ci_task_basic_view.CITaskBasicView.as_view()),
                 url(r"task/list",ci_task_basic_view.CITaskBasicListView.as_view()),
                 url(r"task/my",ci_task_basic_view.CITaskMyListView.as_view()),
                 url(r"project/my",ci_task_basic_view.CIMyProjectView.as_view()),
                 ]


api_task_router=[
                 url(r"task/(?P<task_id>.+)/stages$",ci_task_stage_view.CITaskStageListView.as_view()),
                 url(r"task/(?P<task_id>.+)/config/$",ci_task_stage_view.CITaskConfigView.as_view()),
                 url(r"task/task_stage/(?P<stage_id>.+)/$",ci_task_stage_view.CITaskStageView.as_view()),
                 url(r"task/task_step/(?P<step_id>.+)$",ci_task_stage_view.CITaskStepView.as_view()),
                 url(r"task/task_stage/(?P<stage_id>.+)/steps$",ci_task_stage_view.CITaskStepListView.as_view()),
                 url(r"task/steps$",ci_task_stage_view.CITaskStepTempleteView.as_view()),
                 url(r"task/plugins$",ci_task_basic_view.CITaskPluginListView.as_view()),
                 url(r"task/start$",citask_trigger_view.CITaskTriggerStartView.as_view()),
                 url(r"task/stop$",citask_trigger_view.CITaskTriggerStopView.as_view()),
                 url(r"task_trigger/(?P<tk_uuid>.+)$",citask_trigger_view.CITaskTriggerView.as_view()),
                 url(r"task_triggers$",citask_trigger_view.CITaskTriggerListView.as_view()),
             ]

task_history_router=[
                         url(r"task_history/(?P<history_id>.+)/clean_history$",ci_task_history_view.CITaskHistoryView.as_view()),
                         url(r"task_history/(?P<history_id>.+)/stage_histories/$",ci_task_history_view.CITaskStageHistoryListView.as_view()),
                         url(r"task_history/(?P<history_id>.+)/change_log$",ci_task_history_view.CITaskHistoryChangeLogView.as_view()),
                         url(r"task_history/(?P<id>.+)/$",ci_task_history_view.CITaskHistoryView.as_view()),
                         url(r"task/(?P<task_id>.+)/task_histories/$",ci_task_history_view.CITaskHistoryListView.as_view()),
                         url(r"task/parameter_group/(?P<id>.+)/$",ci_task_parameter_view.CITaskParameterGroupView.as_view()),
                         url(r"task/parameter_group/(?P<id>.+)/copy$",ci_task_parameter_view.CITaskParameterGroupView.as_view()),
                         url(r"task/(?P<task_id>.+)/parameter_groups/$",ci_task_parameter_view.CITaskParameterGroupListView.as_view()),
                         url(r"task/step_status$",ci_task_stage_view.CITaskRunStatusView.as_view()),
                         url(r"task/(?P<taskqueue_id>.+)/done$",ci_task_stage_view.CITaskRunStatusView.as_view()),
                         url(r"task/output/create$",ci_task_stage_view.CITaskOutputListView.as_view()),
                         url(r"task/output/upload$",ci_task_stage_view.CITaskOutputUploadView.as_view()),
                         url(r"task/output/(?P<output_id>.+)/download$",ci_task_stage_view.CITaskOutputDownloadView.as_view()),
                         url(r"task/output/(?P<output_id>.+)/qrcode$",ci_task_stage_view.CITaskOutputQRCodeView.as_view()),
                         url(r"task/output/(?P<output_id>.+)/prepare$",ci_task_stage_view.CITaskOutputDownloadView.as_view()),
                         url(r"task/output/(?P<output_id>.+)/log$",ci_task_history_view.CITaskStepLogView.as_view()),
                         url(r"task/output/log/create$",ci_task_history_view.CITaskStepLogView.as_view()),
                         url(r"task/output/(?P<output_id>.+)$",ci_task_stage_view.CITaskOutputView.as_view()),
                         url(r"task/testresult/export_case_result/(?P<result_id>.+)$",ci_task_history_view.CITaskStepTestResultExportView.as_view()),
                         url(r"task/(?P<task_history_id>.+)/outputs$",ci_task_stage_view.CITaskOutputListView.as_view()),
                         url(r"task/stage_history/(?P<stage_history_id>.+)/$",ci_task_history_view.CITaskStageHistoryView.as_view()),
                         url(r"task/stage_history/(?P<stage_history_id>.+)/logs$",ci_task_history_view.CITaskStageHistoryLogView.as_view()),
                         ]
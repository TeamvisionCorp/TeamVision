#coding=utf-8
# coding=utf-8
'''
Created on 2018-1-5

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.project.serializer import project_task_statistics_serializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.project import models
from teamvision.api.project.viewmodel.project_statistics_charts.vm_task_status_piechart import VM_TaskStatusPieChart
from teamvision.api.project.viewmodel.project_statistics_charts.vm_task_summary_count import  VM_TaskSummaryCount






class TaskStatusPie(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/task_status_pie
    获取每日新增以及解决的bug趋势图
    """
    serializer_class = project_task_statistics_serializer.TaskPieStatisticsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        chart=VM_TaskStatusPieChart(project_id,version_id,self.request)
        return chart


class TaskSummaryCount(generics.RetrieveAPIView):
    """
    /api/project/<project_id>/<version_id>/statistics/task_summary_count
    获取每日新增以及解决的bug趋势图
    """
    serializer_class = project_task_statistics_serializer.TaskSummaryStatisticsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        project_id = self.kwargs.get('project_id', 0)
        version_id = self.kwargs.get('version_id', 0)
        chart = VM_TaskSummaryCount(project_id, version_id,self.request)
        return chart



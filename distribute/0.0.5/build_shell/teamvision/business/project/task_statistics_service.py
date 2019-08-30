#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''

from django.db.models import Count, F

from business.project.task_service import TaskService
from gatesidelib.datetimehelper import DateTimeHelper


class TaskStatisticsService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def task_finished_today(project_id,version_id,request):
        if str(project_id) == "0":
            project_all_tasks=TaskService.all_my_tasks(request,request.user.id)
        else:
            project_all_tasks = TaskService.project_all_tasks(0, project_id)

        if str(version_id)!="0":
            project_all_tasks=project_all_tasks.filter(Version=int(version_id))
        project_all_tasks = project_all_tasks.filter(Parent__isnull=True)
        return project_all_tasks.filter(FinishedDate=DateTimeHelper.get_now_date()).count()

    @staticmethod
    def task_delayed_today(project_id, version_id,request):
        if str(project_id) == "0":
            project_all_tasks=TaskService.all_my_tasks(request,request.user.id)
        else:
            project_all_tasks = TaskService.project_all_tasks(0, project_id)
        project_all_tasks = project_all_tasks.exclude(Status=2).filter(Parent__isnull=True)
        if str(version_id) != "0":
            project_all_tasks = project_all_tasks.filter(Version=int(version_id))
        return project_all_tasks.filter(DeadLine__lt=DateTimeHelper.get_now_date()).count()

    @staticmethod
    def task_delayed_finished_today(project_id, version_id,request):
        if str(project_id) == "0":
            project_all_tasks = TaskService.all_my_tasks(request, request.user.id)
        else:
            project_all_tasks = TaskService.project_all_tasks(0, project_id)
        project_all_tasks = project_all_tasks.filter(Status=2).filter(Parent__isnull=True)
        if str(version_id) != "0":
            project_all_tasks = project_all_tasks.filter(Version=int(version_id))
        return project_all_tasks.filter(DeadLine__lt=F('FinishedDate')).count()


    @staticmethod
    def task_count_bystatus(project_id,version_id,request):
        if str(project_id) == "0":
            project_all_tasks = TaskService.all_my_tasks(request, request.user.id)
        else:
            project_all_tasks = TaskService.project_all_tasks(0, project_id)
        if str(version_id)!="0":
            project_all_tasks=project_all_tasks.filter(Version=int(version_id))
        project_all_tasks = project_all_tasks.filter(Parent__isnull=True)
        result = project_all_tasks.values('Status').annotate(TotalCount=Count('id')).order_by('Status')
        return result

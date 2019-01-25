# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from rest_framework import generics
from doraemon.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from doraemon.project import models
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from doraemon.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from doraemon.api.project.filters import project_filter
from doraemon.api.project.filters.project_pagination import ProjectPagination
from doraemon.api.project.viewmodel.api_project_task import ApiProjectTask
from business.project.task_service import TaskService


class ProjectTaskListView(generics.ListCreateAPIView):
    """
    get:
    /api/project/project_id/project_tasks
    get task list with project_id  FilterSet: Null FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull

    post:
        create new task
    """
    serializer_class = project_serializer.ProjectTaskSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = ProjectPagination


    def get_queryset(self):
        project_id = int(self.kwargs['project_id'])
        version_id = int(self.kwargs['version_id'])
        if str(project_id)!='0':
            if str(version_id)!='0':
                qs=models.Task.objects.get_tasks(project_id).filter(Version=int(version_id)).order_by('-Priority', '-id')
            else:
                qs=models.Task.objects.get_tasks(project_id).order_by('-Priority', '-id')
        else:
            qs=TaskService.all_my_tasks(self.request,'ALL',self.request.user.id)
        return project_filter.ProjectTaskFilterSet(data=self.request.GET, queryset=qs.filter(Parent=None)).filter()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PorjectTaskView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/task/task_id
    get,update,delete task with taskid
    """
    serializer_class = project_serializer.ProjectTaskVMSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        task_id = int(self.kwargs['task_id'])
        task=models.Task.objects.get(task_id)
        temp=ApiProjectTask(task)
        task.Child=temp.Child
        return task

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

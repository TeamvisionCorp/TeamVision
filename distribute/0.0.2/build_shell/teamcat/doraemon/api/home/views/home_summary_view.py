# coding=utf-8
# coding=utf-8
'''
Created on 2018-6-6

@author: ETHAN
'''
from rest_framework import generics
from doraemon.api.home.serializer import home_summary_serializer
from rest_framework.permissions import AllowAny
from doraemon.api.home.viewmodel.api_home_todo_summary import HomeToDoSummary
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from doraemon.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from business.auth_user.log_action_service import LogActionService
from business.project.project_service import ProjectService
from doraemon.api.home.pagination import  home_pagination



class TodoSummaryView(generics.RetrieveAPIView):
    """
    /api/project/task/task_id
    get,update,delete task with taskid
    FilterSet: Null
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=
    """
    serializer_class = home_summary_serializer.ToDoSummarySerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        temp=HomeToDoSummary(self.request)
        return temp


class ActivityListView(generics.ListAPIView):
    """
    /api/project/task/task_id
    get,update,delete task with taskid
    FilterSet: Null
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=
    """
    serializer_class = home_summary_serializer.LogActionSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = home_pagination.HomeActivityPagination

    def get_queryset(self):
        print(self.request.session.items())
        my_projects = ProjectService.get_projects_include_me(self.request)
        my_project_ids = [project.id for project in my_projects]
        all_my_activities = LogActionService.all_project_actions(my_project_ids)
        return all_my_activities

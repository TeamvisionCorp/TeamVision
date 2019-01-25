# coding=utf-8
'''
Created on 2016-8-24

@author: zhangtiande
'''
from business.project.task_service import TaskService
from business.project.fortesting_service import ForTestingService
from business.project.project_service import ProjectService
from doraemon.project.models import ProjectIssue


class HomeToDoSummary(object):
    '''
    classdocs
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        self.request = request
        self.task_count = self.task_count()
        self.issue_count = self.issue_count()
        self.fortesting_count = self.fortesting_count()

    def task_count(self):
        all_my_tasks = TaskService.all_my_tasks(self.request,'ALL',self.request.user.id)
        all_my_tasks = all_my_tasks.filter(Status__in=(0,1)).filter(Parent=None)
        return len(all_my_tasks)

    def issue_count(self):
        all_my_issue = ProjectIssue.objects.get_processor_issue(self.request.user.id)
        return len(all_my_issue.filter(Status__in=(1,2)))

    def fortesting_count(self):
        my_projects = ProjectService.get_projects_include_me(self.request)
        my_project_ids =  [project.id for project in my_projects]
        my_fortesting = ForTestingService.get_projects_fortestings(my_project_ids).filter(Status=2)
        return len(my_fortesting)
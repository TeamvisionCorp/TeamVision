#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.home.pagefactory.pageworker import DevicePageWorker
from doraemon.home.viewmodels.home_left_nav_bar import HomeDashboardLeftNavBar
from doraemon.home.pagefactory.home_template_path import HomeDashBoardPath
from doraemon.home.pagefactory.home_project_pageworker import HomeProjectPageWorker
from doraemon.project.pagefactory.project_task_pageworker import ProjectTaskPageWorker
from doraemon.project.pagefactory.project_fortesting_pageworker import ProjectForTestingPageWorker
from doraemon.project.pagefactory.project_dashboard_pageworker import ProjectDashBoardPageWorker

from business.auth_user.log_action_service import LogActionService
from business.project.project_service import ProjectService
from business.project.task_service import TaskService
from business.project.fortesting_service import ForTestingService

class HomeDashBoardPageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.pagemodel=HomeDashboardLeftNavBar
    
    def get_dashboard_fullpage(self,request):
        left_nav_bar=self.get_dashboard_left_bar(request)
        summary=self.get_dashboard_summary(request)
        activity=self.get_dashboard_activity(request)
        pagefileds={"left_nav_bar":left_nav_bar,"dashboard_summary":summary,"dashboard_activity":activity}
        return self.get_page(pagefileds,'dashboard/home_dashboard_index.html',request)
    
    
    def get_dashboard_left_bar(self,request):
        return self.get_left_nav_bar(request,self.pagemodel,HomeDashBoardPath.left_nav_template_path)
    
    def get_dashboard_activity(self,request):
        all_activity_webpart=self.get_project_activites(request,0)
        device_activity_webpart=self.get_device_activites(request,0)
        pagefileds={"all_activity_webpart":all_activity_webpart,"device_activity_webpart":device_activity_webpart}
        return self.get_webpart(pagefileds,HomeDashBoardPath.activity_template_path)
    
    
    def get_more_activites(self,request,start_index,activity_type):
        activity_webpart=""
        if activity_type.upper()=="#ALL":
            activity_webpart=self.get_project_activites(request, start_index)
        if activity_type.upper()=="#DEVICE":
            activity_webpart=self.get_device_activites(request, start_index)
        return activity_webpart
    
    def get_device_activites(self,request,start_index):
        page_worker=ProjectDashBoardPageWorker(request)
        projectids=[-1]
        log_actions=LogActionService.all_project_actions(projectids)[start_index:(start_index+20)]
        activity_webpart=page_worker.get_activity_webpart(log_actions,False,request.user)
        return activity_webpart
    
    def get_project_activites(self,request,start_index):
        page_worker=ProjectDashBoardPageWorker(request)
        projectids=[project.id for project in ProjectService.get_projects_include_me(request)]
        log_actions=LogActionService.all_project_actions(projectids)[start_index:(start_index+20)]
        activity_webpart=page_worker.get_activity_webpart(log_actions,False,request.user)
        return activity_webpart
#     
    def get_dashboard_summary(self,request):
        dashboard_project_list=self.get_project_summary(request)
        dashboard_task_list=self.get_task_summary(request)
        dashboard_fortesting_list=self.get_fortesting_summary(request)
        pagefileds={"dashboard_project_list":dashboard_project_list,"dashboard_task_list":dashboard_task_list,'dashboard_fortesting_list':dashboard_fortesting_list}
        return self.get_webpart(pagefileds,HomeDashBoardPath.summary_template_path)
    
    def get_project_summary(self,request):
        page_worker=HomeProjectPageWorker(request)
        dm_projects=ProjectService.get_latest_projects(request)[0:8]
        dashboard_project_list=page_worker.get_home_dashboard_project_list(request,dm_projects)
        return dashboard_project_list
    
    def get_task_summary(self,request):
        task_list=TaskService.all_tasks(request,"all")[0:5]
        page_worker=ProjectTaskPageWorker(request)
        dashboard_task_list=page_worker.get_task_listcontrol(task_list, True,False, False)
        return dashboard_task_list
    
    def get_fortesting_summary(self,request):
        page_worker=ProjectForTestingPageWorker(request)
        project_ids=[project.id for project in ProjectService.get_projects_include_me(request)]
        fortestings=ForTestingService.get_projects_fortestings(project_ids)[0:5]
        dashboard_fortesting_list=page_worker.get_fortesting_list_controll(True,False,fortestings)
        return dashboard_fortesting_list
        
        
        
        
    
#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.project.pagefactory.project_pageworker import ProjectPageWorker
from doraemon.project.viewmodels.project_left_nav_bar import ProjectDashboardLeftNavBar
from doraemon.project.pagefactory.project_template_path import ProjectDashBoardPath
from doraemon.project.pagefactory.project_task_pageworker import ProjectTaskPageWorker
from doraemon.project.pagefactory.project_fortesting_pageworker import ProjectForTestingPageWorker
from business.project.task_service import TaskService
from business.project.fortesting_service import ForTestingService
from business.auth_user.log_action_service import LogActionService
from doraemon.auth_extend.user.viewmodels.vm_action_log import VM_ActionLog

class ProjectDashBoardPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.pagemodel=ProjectDashboardLeftNavBar
    
    def get_dashboard_left_bar(self,request,projectid):
        return self.get_left_nav_bar(request,self.pagemodel,projectid,ProjectDashBoardPath.left_nav_template_path)
    
    def get_dashboard_activity(self,request,projectid):
        activity_webpart=self.get_more_activites(request,projectid,0)
        pagefileds={"activity_webpart":activity_webpart}
        return self.get_webpart(pagefileds,ProjectDashBoardPath.activity_template_path)
    
    def get_more_activites(self,request,project_id,start_index):
        log_actions=LogActionService.project_actions(project_id)[start_index:start_index+20]
        activity_webpart=self.get_activity_webpart(log_actions,True,request.user)
        return activity_webpart
    
    def get_activity_webpart(self,log_actions,is_fullpart,login_user):
        project_activities=self.get_project_activities(log_actions,is_fullpart,login_user)
        pagefileds={"actions":project_activities}
        result=self.get_webpart(pagefileds,ProjectDashBoardPath.activity_webpart_path)
        return result
        
#     
    def get_dashboard_items(self,request,projectid):
        project_dashboard_task=self.get_dashboard_tasks(request,projectid)
        project_dashboard_fortesting=self.get_dashboard_fortesting(projectid,request.user.id,request)
        pagefileds={'project_dashboard_task':project_dashboard_task,'projectid':projectid,'project_dashboard_fortesting':project_dashboard_fortesting}
        return self.get_webpart(pagefileds,ProjectDashBoardPath.project_item_template_path)
    
    
    def get_dashboard_tasks(self,request,projectid):
        task_list=TaskService.project_all_tasks(request,projectid,"all")[0:5]
        page_worker=ProjectTaskPageWorker(request)
        return page_worker.get_task_listcontrol(task_list,False,False,False)
    
    def get_dashboard_fortesting(self,projectid,userid,request):
        page_worker=ProjectForTestingPageWorker(request)
        dm_fortestings=ForTestingService.get_project_fortestings(projectid)[0:5]
        return page_worker.get_fortesting_list_controll(False,False,dm_fortestings)
    
    def get_project_activities(self,log_actions,is_fullpart,login_user):
        result=list();
        for log_action in log_actions:
            tmp_log_action=VM_ActionLog(log_action,is_fullpart,login_user)
            result.append(tmp_log_action)
        return result
            
        
        
        
        
    
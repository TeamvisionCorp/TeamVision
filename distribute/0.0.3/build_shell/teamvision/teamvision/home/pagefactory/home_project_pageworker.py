#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.home.pagefactory.pageworker import DevicePageWorker
from teamvision.home.viewmodels.home_left_nav_bar import HomeProjectLeftNavBar
from teamvision.home.viewmodels.home_sub_nav_bar import HomeProjectSubNavBar
from teamvision.home.pagefactory.home_template_path import HomeProjectPath
from teamvision.project.viewmodels.vm_project import VM_Project

from business.project.project_service import ProjectService

class HomeProjectPageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.pagemodel=HomeProjectLeftNavBar
        self.sub_sidebar_model=HomeProjectSubNavBar
        
    
    def get_project_fullpage(self,request,sub_nav_action):
        dm_projects=ProjectService.get_projects_include_me(request,sub_nav_action)
        dm_products=ProjectService.get_products_include_me(request)
        left_nav_bar=self.get_project_left_bar(request, sub_nav_action)
        sub_nav_bar=self.get_project_sub_nav_bar(request,dm_projects,sub_nav_action,dm_products)
        project_list=self.get_project_list_page(request,dm_projects)
        pagefileds={'left_nav_bar':left_nav_bar,"sub_nav_bar":"","project_list":project_list}
        return self.get_page(pagefileds,'project/home_project_index.html',request)
    
    def get_project_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.pagemodel,HomeProjectPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    
    def get_project_sub_nav_bar(self,request,dm_projects,sub_nav_action,products):
        return self.get_sub_nav_bar(request,self.sub_sidebar_model,HomeProjectPath.sub_nav_template_path,sub_nav_action=sub_nav_action,projects=dm_projects,products=products)
    
    def get_project_list_page(self,request,dm_projects):
        projects=list()
        for project in dm_projects:
            tem_project=VM_Project(request.user,False,project,0)
            projects.append(tem_project)
        project_list_control=self.get_project_control(request, projects)
        pagefileds={"projects":projects,"project_list":project_list_control}
        return self.get_webpart(pagefileds,HomeProjectPath.project_list_template_path)
    
    def get_home_dashboard_project_list(self,request,dm_projects):
        projects=list()
        for project in dm_projects:
            if project !=None:
                tem_project=VM_Project(request.user,False,project,0)
                projects.append(tem_project)
        project_list_control=self.get_project_control(request, projects)
        return project_list_control
        
    
    def get_project_control(self,request,projects):
        pagefileds={"projects":projects}
        return self.get_webpart(pagefileds,HomeProjectPath.project_list_control_path)
        
        
        
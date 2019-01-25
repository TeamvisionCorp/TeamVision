#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.project.pagefactory.project_pageworker import ProjectPageWorker
from doraemon.project.viewmodels.project_left_nav_bar import ProjectVersionLeftNavBar
from doraemon.project.viewmodels.project_sub_nav_bar import ProjectVersionSubNavBar
from doraemon.project.pagefactory.project_template_path import ProjectVersionPath
from doraemon.project.models import Version
from doraemon.project.viewmodels.vm_project_version import VM_ProjectVersion




class ProjectVersionPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.left_nav_bar_model=ProjectVersionLeftNavBar
        self.subpage_model=ProjectVersionSubNavBar
    
    def get_full_page(self,request,projectid):
#         sub_leftnav=self.get_version_sub_navbar(request,projectid)
        left_nav_bar=self.get_version_left_bar(request,projectid)
        version_list=self.get_version_list_page(projectid);
        pagefileds={'left_nav_bar':left_nav_bar,'version_list':version_list}
        return self.get_full_page_with_header(request, pagefileds, projectid,'versions/index.html')
    
    
    def get_version_left_bar(self,request,projectid):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,projectid,ProjectVersionPath.left_nav_template_path)
    
    def get_version_sub_navbar(self,request,projectid, sub_nav_action):
        return self.get_sub_nav_bar(request, self.subpage_model, projectid,ProjectVersionPath.version_sub_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_version_list_page(self,projectid):
        version_list_controll=self.get_version_list_controll(projectid)
        context_fileds={'version_list_controll':version_list_controll}
        return self.get_webpart(context_fileds,ProjectVersionPath.version_list_page_path)
    
    def get_version_list_controll(self,projectid):
        versions=self.get_versions(projectid)
        context_fileds={'versions':versions}
        return self.get_webpart(context_fileds,ProjectVersionPath.version_list_controll_path)
    def get_versions(self,projectid):
        version_list=list()
        for version in Version.objects.all().filter(VProjectID=projectid).order_by("-id"):
            temp_version=VM_ProjectVersion(version)
            version_list.append(temp_version)
        return version_list
        
        
    

        
    
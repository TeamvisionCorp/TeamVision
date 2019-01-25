#coding=utf-8

'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.home.pagefactory.pageworker import DevicePageWorker
from doraemon.home.viewmodels.home_left_nav_bar import HomeIssueLeftNavBar
from doraemon.home.viewmodels.home_sub_nav_bar import HomeIssueSubNavBar
from doraemon.home.pagefactory.home_template_path import HomeIssuePath
from doraemon.project.pagefactory.project_issue_pageworker import ProjectIssuePageWorker
from business.project.issue_service import IssueService
from business.project.project_service import ProjectService


class HomeIssuePageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.left_nav_bar_model=HomeIssueLeftNavBar
        self.subpage_model=HomeIssueSubNavBar
    
    def  get_full_page(self,request, sub_nav_action):
        project_ids=[project.id for project in ProjectService.get_projects_include_me(request)]
        left_nav_bar=self.get_issue_left_bar(request,sub_nav_action)
        issue_webpart=self.get_issue_webpart(request,sub_nav_action)
        page_fileds={'left_nav_bar':left_nav_bar,'issue_webpart':issue_webpart}
        return self.get_page(page_fileds,HomeIssuePath.home_issue_index,request)
    
    def get_issue_webpart(self,request,user_role):
        issue_page_worker=ProjectIssuePageWorker(request)
        issue_list=issue_page_worker.get_my_issue_item(request.user.id,user_role)
        sub_leftnav=self.get_issue_sub_navbar(request,user_role)
        page_fileds={'issue_list':issue_list,'sub_leftnav':sub_leftnav}
        return self.get_webpart(page_fileds,HomeIssuePath.home_issue_webapp)
    
    
        
    
    def get_issue_left_bar(self,request, sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,HomeIssuePath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_issue_sub_navbar(self,request,sub_nav_action):
        issues=IssueService.my_issue(request.user.id,sub_nav_action)
        return self.get_sub_nav_bar(request, self.subpage_model,HomeIssuePath.sub_nav_template_path,sub_nav_action=sub_nav_action,issues=issues)
    

        
    
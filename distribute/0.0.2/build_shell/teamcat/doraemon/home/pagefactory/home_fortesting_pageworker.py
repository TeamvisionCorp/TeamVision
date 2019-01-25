#coding=utf-8

'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.home.pagefactory.pageworker import DevicePageWorker
from doraemon.home.viewmodels.home_left_nav_bar import HomeForTestingLeftNavBar
from doraemon.home.viewmodels.home_sub_nav_bar import HomeFortestingSubNavBar
from doraemon.home.pagefactory.home_template_path import HomeFortestingPath
from doraemon.project.pagefactory.project_fortesting_pageworker import ProjectForTestingPageWorker
from business.project.fortesting_service import ForTestingService
from business.project.project_service import ProjectService


class HomeForTestingPageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.left_nav_bar_model=HomeForTestingLeftNavBar
        self.subpage_model=HomeFortestingSubNavBar
    
    def get_full_page(self,request, sub_nav_action):
        project_ids=[project.id for project in ProjectService.get_projects_include_me(request)]
        sub_leftnav=self.get_fortesting_sub_navbar(request,project_ids,sub_nav_action)
        left_nav_bar=self.get_fortesting_left_bar(request,sub_nav_action)
        project_page_worker=ProjectForTestingPageWorker(request)
        fortestings=ForTestingService.get_projects_fortestings(project_ids)
        fortesting_list=project_page_worker.get_fortesting_list_page(True,False,fortestings)
        page_fileds={'left_nav_bar':left_nav_bar,'sub_leftnav':"",'fortesting_list':fortesting_list}
        return self.get_page(page_fileds,'fortesting/index.html',request)
    
        
    
    def get_fortesting_left_bar(self,request, sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,HomeFortestingPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_fortesting_sub_navbar(self,request,project_ids,sub_nav_action):
        fortestings=ForTestingService.get_projects_fortestings(project_ids)
        return self.get_sub_nav_bar(request, self.subpage_model,HomeFortestingPath.sub_nav_template_path,sub_nav_action=sub_nav_action,fortestings=fortestings)
    

        
    
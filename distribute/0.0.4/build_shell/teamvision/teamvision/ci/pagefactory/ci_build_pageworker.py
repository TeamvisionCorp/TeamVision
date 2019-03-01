#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.ci.pagefactory.ci_task_pageworker import CITaskPageWorker

from teamvision.ci.viewmodels.ci_left_nav_bar import CIBuildLeftNavBar
from teamvision.ci.viewmodels.ci_sub_nav_bar import CIBuildTaskSubNavBar
from teamvision.ci.viewmodels.ci_task_property_nav_bar import CITaskPropertyNavBar
from teamvision.ci.pagefactory.ci_template_path import CITaskPath
from business.ci.ci_task_service import CITaskService
from teamvision.ci.pagefactory.ci_testing_pageworker import CITestingPageWorker
from django.shortcuts import render_to_response
from django.template import RequestContext




class CIBuildPageWorker(CITaskPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        CITaskPageWorker.__init__(self, request)
        self.pagemodel = CIBuildLeftNavBar
        self.subpage_model = CIBuildTaskSubNavBar
        self.task_property_model=CITaskPropertyNavBar
    
    def get_build_fullpage(self, request, sub_nav_action):
        return self.get_ci_task_fullpage(request, 4, sub_nav_action)
        
    
    def get_build_history_fullpage(self, request,task_id,task_property):
        return self.get_task_history_fullpage(request, task_id, task_property)
    
    
    def get_unittest_history_fullpage(self, request,task_id,task_property):
        dm_products = CITaskService.get_products_include_me(request)
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request,dm_products,0,task_id,task_property)
        test_pageworker=CITestingPageWorker(request)
        ci_task_history_webpart = test_pageworker.ci_testing_history_webpart(request, task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_task_history":ci_task_history_webpart}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    
    def build_history_clean_fullpage(self, request,task_id,task_property):
        return self.history_clean_fullpage(request, task_id, task_property)
    
    def get_build_changelog_fullpage(self, request,task_id,task_property):
        return self.get_task_changelog_fullpage(request, task_id, task_property)
    
    def get_build_parameter_fullpage(self, request,task_id,task_property):
        return self.get_task_parameter_fullpage(request, task_id, task_property)
    
    
    def get_build_task_config_page(self, request, task_id,task_property):
        return self.get_ci_task_config_page(request, task_id,task_property)
    
    
        
        
        
        
    

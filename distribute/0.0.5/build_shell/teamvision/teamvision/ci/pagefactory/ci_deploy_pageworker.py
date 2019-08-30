#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.ci.pagefactory.ci_pageworker import CIPageWorker
from teamvision.ci.pagefactory.ci_task_pageworker import CITaskPageWorker
from teamvision.ci.viewmodels.ci_left_nav_bar import CIDeployLeftNavBar
from teamvision.ci.viewmodels.ci_sub_nav_bar import CIDeployTaskSubNavBar
from teamvision.ci.viewmodels.ci_task_property_nav_bar import CITaskPropertyNavBar
from teamvision.ci.pagefactory.ci_template_path import CITaskPath
from business.ci.ci_task_service import CITaskService
from django.shortcuts import render_to_response
from django.template import RequestContext





class CIDeployPageWorker(CITaskPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        CITaskPageWorker.__init__(self, request)
        self.pagemodel = CIDeployLeftNavBar
        self.subpage_model = CIDeployTaskSubNavBar
        self.task_property_model=CITaskPropertyNavBar
    
    def get_deploy_fullpage(self, request, sub_nav_action):
        return self.get_ci_task_fullpage(request, 5, sub_nav_action)
    
    def get_deploy_history_fullpage(self, request,task_id,task_property):
        return self.get_task_history_fullpage(request, task_id, task_property)
    
    def get_deploy_changelog_fullpage(self, request,task_id,task_property):
        return self.get_task_changelog_fullpage(request, task_id, task_property)
    
    def history_clean_fullpage(self, request,task_id,task_property):
        return self.history_clean_fullpage(request, task_id, task_property)
    
    def get_deploy_parameter_fullpage(self, request,task_id,task_property):
        return self.get_task_parameter_fullpage(request, task_id, task_property)
    
    def get_deploy_task_config_page(self, request, task_id,task_property):
        return self.get_ci_task_config_page(request, task_id,task_property)
    
    
    
    
        
        
        
        
    

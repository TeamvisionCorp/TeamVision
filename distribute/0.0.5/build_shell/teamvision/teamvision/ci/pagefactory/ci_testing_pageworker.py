#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.ci.pagefactory.ci_task_pageworker import CITaskPageWorker
from teamvision.ci.viewmodels.ci_left_nav_bar import CITestingLeftNavBar
from teamvision.ci.viewmodels.ci_sub_nav_bar import CITestingTaskSubNavBar
from teamvision.ci.viewmodels.ci_task_property_nav_bar import CITestingTaskPropertyNavBar
from teamvision.ci.pagefactory.ci_template_path import CITaskPath,TestingTaskPath
from teamvision.ci.models import CITask,AutoTestingTaskResult,AutoCaseResult,UnitTestCaseResult
from teamvision.ci.viewmodels.vm_ci_task import VM_CITask
from teamvision.ci.viewmodels.vm_ci_task_history import VM_CITaskHistory
from teamvision.ci.viewmodels.vm_auto_case_result import VM_AutoCaseResult
from business.ci.ci_task_service import CITaskService
from business.ci.ci_task_history_service import CITaskHistoryService
from django.shortcuts import render_to_response
from django.template import RequestContext




class CITestingPageWorker(CITaskPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        CITaskPageWorker.__init__(self, request)
        self.pagemodel = CITestingLeftNavBar
        self.subpage_model = CITestingTaskSubNavBar
        self.task_property_model=CITestingTaskPropertyNavBar
    
    def testing_fullpage(self, request, sub_nav_action):
        return self.get_ci_task_fullpage(request, 1, sub_nav_action)
        
    
    def testing_result_fullpage(self, request,task_id,task_property):
        return self.get_task_history_fullpage(request, task_id, task_property)
    
    def get_task_history_fullpage(self, request,task_id,task_property):
        dm_products = CITaskService.get_products_include_me(request)
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request,dm_products,0,task_id,task_property)
        ci_task_history_webpart = self.ci_testing_history_webpart(request,task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_task_history":ci_task_history_webpart}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    
    def ci_testing_history_webpart(self, request,task_id):
        task_historys=CITaskHistoryService.get_finished_history(task_id)
        first_history_id=0
        first_history=None
        if len(task_historys):
            first_history=task_historys[0]
            first_history_id=task_historys[0].id
        testing_history_result_list = self.ci_testing_history_list(task_id)
        testing_history_analytics=self.testing_history_analytics(first_history_id)
        testing_case_result_list=self.testing_case_result_list(first_history_id,0,count=20)
        ci_task=CITask.objects.get(int(task_id))
        pagefileds = {"testing_history_result_list":testing_history_result_list,"ci_task":ci_task}
        pagefileds['testing_history_analytics']=testing_history_analytics
        pagefileds['testing_case_result_list']=testing_case_result_list
        pagefileds['ci_history']=first_history
        return self.get_webpart(pagefileds,TestingTaskPath.teting_history_page)
    
    def ci_testing_history_list(self,task_id):
        dm_task_histories=dm_task_histories=CITaskHistoryService.get_finished_history(task_id)
        vm_task_histories=list()
        for history in dm_task_histories:
            temp_history=VM_CITaskHistory(history,None)
            vm_task_histories.append(temp_history)
        pagefileds = {"ci_task_histories":vm_task_histories}
        return self.get_webpart(pagefileds, TestingTaskPath.testing_history_list)
    
    def testing_history_analytics(self,history_id):
        task_result=AutoTestingTaskResult.objects.get_by_historyid(history_id)
        pagefileds = {"auto_task_result":task_result}
        return self.get_webpart(pagefileds, TestingTaskPath.teting_analytics_webpart)
    
    def testing_case_result_list(self,history_id,result_type,count=50):
        task_result=AutoTestingTaskResult.objects.get_by_historyid(history_id)
        auto_case_results=list()
        if task_result:
            auto_case_results=AutoCaseResult.objects.get_by_resultid(task_result.id,result_type)[:count]
            if not auto_case_results:
                auto_case_results=UnitTestCaseResult.objects.get_by_task_result(task_result.id,result_type)[:count]
        vm_case_results=list()
        for case_result in auto_case_results:
            temp_case_result=VM_AutoCaseResult(case_result)
            vm_case_results.append(temp_case_result)
        pagefileds = {"auto_case_results":vm_case_results}
        return self.get_webpart(pagefileds, TestingTaskPath.teting_caseresult_list)
    
    
    
    def testing_history_clean_fullpage(self, request,task_id,task_property):
        return self.history_clean_fullpage(request, task_id, task_property)
    
    
    def testing_parameter_fullpage(self, request,task_id,task_property):
        return self.get_task_parameter_fullpage(request, task_id, task_property)
    
    
    def testing_task_config_page(self, request, task_id,task_property):
        return self.get_ci_task_config_page(request, task_id,task_property)
    
    def get_task_sub_navbar(self, request, dm_products,sub_nav_action,task_id=0,task_property=None):
        if sub_nav_action:
            result=self.get_sub_nav_bar(request, self.subpage_model, CITaskPath.sub_nav_template_path, sub_nav_action=sub_nav_action, products=dm_products)
        else:
            dm_ci_task = CITask.objects.get(task_id)
            vm_ci_task = VM_CITask(dm_ci_task, None, False,True)
            result=self.get_property_nav_bar(request, self.task_property_model,CITaskPath.testing_property_nav,property_nav_action=task_property,ci_task=vm_ci_task)
        return result
        
        
        
        
    

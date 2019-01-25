#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.ci.pagefactory.ci_pageworker import CIPageWorker
from doraemon.ci.viewmodels.ci_left_nav_bar import CIServiceLeftNavBar
from doraemon.ci.viewmodels.ci_sub_nav_bar import CIServiceSubNavBar
from doraemon.ci.viewmodels.vm_ci_deploy_service import VM_CIDeployService
from doraemon.ci.pagefactory.ci_template_path import CIServicePath
from doraemon.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from business.ci.ci_service import CIService
from doraemon.ci.models import CIDeployService


class CIServicePageWorker(CIPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        CIPageWorker.__init__(self, request)
        self.pagemodel = CIServiceLeftNavBar
        self.subpage_model = CIServiceSubNavBar
    
    def get_ci_service_fullpage(self, request,sub_nav_action):
        dm_products = CIService.get_products_include_me(request)
        left_nav_bar = self.get_service_left_bar(request)
        sub_nav_bar = self.get_service_sub_navbar(request, dm_products, sub_nav_action)
        ci_service_webpart = self.get_ci_service_list_webpart(request,sub_nav_action)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_service_webpart":ci_service_webpart}
        return self.get_page(page_fileds,CIServicePath.service_index_path, request)
    
    def get_ci_service_config_page(self, request,service_id):
        dm_products = CIService.get_products_include_me(request)
        left_nav_bar = self.get_service_left_bar(request)
        sub_nav_bar = self.get_service_sub_navbar(request, dm_products,0)
        ci_service_config_webpart = self.ci_service_config_webpart(request,service_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_service_config":ci_service_config_webpart}
        return self.get_page(page_fileds,CIServicePath.service_index_path,request)
    
    
    def ci_service_config_webpart(self, request,service_id):
        service=CIDeployService.objects.get(int(service_id))
        vm_service=VM_CIDeployService(service,0)
        ci_service_project=ProjectCommonControllPageWorker.get_myproject_dropdown_list(self, request,service.Project)
        pagefileds = {"service":vm_service,"ci_service_project":ci_service_project}
        return self.get_webpart(pagefileds, CIServicePath.service_config_page)
    
         
    def get_ci_service_list_webpart(self, request,sub_nav_action):
        service_list_controll = self.get_ci_service_list_controll(request, sub_nav_action)
        pagefileds = {"ci_service_listcontroll":service_list_controll}
        return self.get_webpart(pagefileds, CIServicePath.service_list_webpart)
    
    def get_ci_service_list_controll(self, request,sub_nav_action):
        dm_ci_services = CIService.get_product_ci_services(request,sub_nav_action)
        ci_services = self.get_ci_services(request, dm_ci_services)
        pagefileds = {"ci_services":ci_services}
        return self.get_webpart(pagefileds, CIServicePath.service_list_controll)
    
    
    def get_service_left_bar(self, request):
        return self.get_left_nav_bar(request, self.pagemodel, CIServicePath.left_nav_template_path)
    
    def get_service_sub_navbar(self, request, dm_products, sub_nav_action):
        return self.get_sub_nav_bar(request, self.subpage_model, CIServicePath.sub_nav_template_path, sub_nav_action=sub_nav_action, products=dm_products)
    
    def get_ci_services(self,request,dm_ci_services):
        result=list()
        for service in dm_ci_services:
            temp=VM_CIDeployService(service,0)
            result.append(temp)
        return result
        
        
        
        
    

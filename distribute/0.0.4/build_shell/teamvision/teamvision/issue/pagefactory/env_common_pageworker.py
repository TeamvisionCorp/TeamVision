#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.interface.pagefactory.env_pageworker import ENVPageWorker
from teamvision.project.pagefactory.project_template_path import ProjectCommonControllPath
from teamvision.project.models import Project,Product
from teamvision.project.viewmodels.vm_project import VM_Project
from teamvision.project.viewmodels.vm_project_module import VM_ProjectModule
from teamvision.project.viewmodels.vm_product import VM_Product
from teamvision.project.viewmodels.vm_platform import VM_Platform
from business.common.system_config_service import SystemConfigService
from business.project.project_service import ProjectService
from business.project.version_service import VersionService
from teamvision.project.viewmodels.vm_project_version import VM_ProjectVersion

class ENVCommonControllPageWorker(ENVPageWorker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        '''
        Constructor
        '''
        ENVPageWorker.__init__(self, request)
    
    
    
    def get_project_dropdown_list(self,userid,selected_project_id):
        vm_projects=list()
        for dm_project in Project.objects.all():
            tem_project=VM_Project(userid,False,dm_project,selected_project_id)
            vm_projects.append(tem_project)
        pagefileds={"projects":vm_projects}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.project_dropdown_list_path)
    
    
    def get_myproject_dropdown_list(self,request,selected_project_id):
        vm_projects=list()
        for dm_project in ProjectService.get_projects_include_me(request):
            tem_project=VM_Project(request.user.id,False,dm_project,selected_project_id)
            vm_projects.append(tem_project)
        pagefileds={"projects":vm_projects}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.project_dropdown_list_path)
    
    
    def get_module_dropdown_list(self,project_id,selected_module_id):
        vm_modules=list()
        for dm_module in ProjectService.get_project_modules(project_id):
            tem_module=VM_ProjectModule(dm_module,selected_module_id)
            vm_modules.append(tem_module)
        pagefileds={"modules":vm_modules}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.module_dropdown_list_path)
    
    
    def get_version_dropdown_list(self,project_id):
        vm_versions=list()
        print(1)
        for dm_version in VersionService.get_project_version(project_id):
            print(dm_version.id)
            temp_version=VM_ProjectVersion(dm_version)
            vm_versions.append(temp_version)
        pagefileds={"versions":vm_versions}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.version_dropdown_list_path)
    
    
    def get_platform_dropdown_list(self,project_id):
        vm_platforms=list()
        platform_value=0
        platforms=SystemConfigService.get_platform_configs()
        if project_id:
            platform_value=Project.objects.get(project_id).PBPlatform
        for platform in platforms:
            tmp_platfrom=VM_Platform(platform,platform_value)
            vm_platforms.append(tmp_platfrom)
            
        pagefileds={"platforms":vm_platforms}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.platform_dropdown_list_path)
    
    
    def get_product_dropdown_list(self,userid,selected_product_id):
        vm_products=list()
        for dm_product in Product.objects.all():
            tem_product=VM_Product(userid,dm_product,selected_product_id)
            vm_products.append(tem_product)
        pagefileds={"products":vm_products}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.product_dropdown_list_path)
            
            
        
        
        
        
        
    
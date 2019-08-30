#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.project.pagefactory.project_pageworker import ProjectPageWorker
from teamvision.project.pagefactory.project_template_path import ProjectCommonControllPath
from teamvision.project.models import Project,Product,ProjectOSVersion
from teamvision.project.viewmodels.vm_project import VM_Project
from teamvision.project.viewmodels.vm_project_module import VM_ProjectModule
from teamvision.project.viewmodels.vm_product import VM_Product
from teamvision.project.viewmodels.vm_platform import VM_Platform
from business.common.system_config_service import SystemConfigService
from business.project.project_service import ProjectService
from business.project.version_service import VersionService
from teamvision.project.viewmodels.vm_project_version import VM_ProjectVersion
from teamvision.project.viewmodels.vm_project_member import VM_ProjectMember
from teamvision.project.viewmodels.vm_project_issue_field import VM_IssueField
from teamvision.project.viewmodels.vm_team import VM_Team
from teamvision.project.models import Project,ProjectRole,ProjectMember
from teamvision.home.models import Team

class ProjectCommonControllPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
    
    
    
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
        default="<option value=\"0\">无</option>"
        vm_modules=list()
        for dm_module in ProjectService.get_project_modules(project_id):
            tem_module=VM_ProjectModule(dm_module,selected_module_id)
            vm_modules.append(tem_module)
        pagefileds={"modules":vm_modules}
        return default+self.get_webpart(pagefileds,ProjectCommonControllPath.module_dropdown_list_path)
    
    def get_module_dropdown_menu(self,project_id,selected_module_id):
        vm_modules=list()
        for dm_module in ProjectService.get_project_modules(project_id):
            tem_module=VM_ProjectModule(dm_module,selected_module_id)
            vm_modules.append(tem_module)
        pagefileds={"modules":vm_modules}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.module_dropdown_menu)


    def get_team_dropdown_list(self,selected_team_id):
        default="<option value=\"0\">无</option>"
        vm_teams=list()
        for dm_team in Team.objects.all():
            temp_team=VM_Team(dm_team,selected_team_id)
            vm_teams.append(temp_team)
        pagefileds={"teams":vm_teams}
        return default+self.get_webpart(pagefileds,ProjectCommonControllPath.team_dropdown_list_path)

    def get_team_dropdown_menu(self,selected_team_id):
        vm_teams=list()
        for dm_team in Team.objects.all():
            temp_team=VM_Team(dm_team,selected_team_id)
            vm_teams.append(temp_team)
        pagefileds={"teams":vm_teams}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.team_dropdown_menu)
    
    def get_version_dropdown_list(self,project_id,selected_version=0,default_none=True):
        if str(selected_version)=="0":
            default="<option selected value=\"0\">无</option>"
        else:
            default="<option  value=\"0\">无</option>"
        vm_versions=list()
        for dm_version in VersionService.get_project_version(project_id):
            temp_version=VM_ProjectVersion(dm_version,selected_version)
            vm_versions.append(temp_version)
        pagefileds={"versions":vm_versions}
        if default_none:
            result=default+self.get_webpart(pagefileds,ProjectCommonControllPath.version_dropdown_list_path)
        else:
            result=self.get_webpart(pagefileds,ProjectCommonControllPath.version_dropdown_list_path)
        return result
    
    def get_version_dropdown_menu(self,project_id,selected_version):
        vm_versions=list()
        for dm_version in VersionService.get_project_version(project_id):
            temp_version=VM_ProjectVersion(dm_version,selected_version)
            vm_versions.append(temp_version)
        pagefileds={"versions":vm_versions}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.version_dropdown_menu)
    
    
    def get_issue_upload_dropdown_menu(self):
        return self.get_webpart_none_args(ProjectCommonControllPath.issue_upload_menu)
    
    
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
    
    def get_issue_field_dropdown_list(self,field_model,selected_field_value):
        vm_fields=list()
        for dm_field in field_model.objects.all():
            temp_field=VM_IssueField(dm_field,selected_field_value)
            vm_fields.append(temp_field)
        pagefileds={"fields":vm_fields}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.issue_field_dropdown_list)
    
    def get_issue_field_dropdown_menu(self,field_model,selected_field_value):
        vm_fields=list()
        for dm_field in field_model.objects.all():
            temp_field=VM_IssueField(dm_field,selected_field_value)
            vm_fields.append(temp_field)
        pagefileds={"fields":vm_fields}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.issue_field_dropdown_menu)
    
    def get_issue_device_version_dropdown_menu(self,device_os,selected_field_value):
        vm_fields=list()
        for dm_field in ProjectOSVersion.objects.get_by_os(int(device_os)):
            temp_field=VM_IssueField(dm_field,selected_field_value)
            vm_fields.append(temp_field)
        pagefileds={"fields":vm_fields}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.issue_field_dropdown_menu)
    
    
    
    def get_user_listbox(self,users,project_id):
        vm_users=list()
        for user in users:
            tmp_user=VM_ProjectMember(project_id,user,None,None)
            vm_users.append(tmp_user)
        pagefileds={"members":vm_users}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.user_listbox_path)
    
    
    def get_member_dropdownlist(self,users,project_id,selected_member):
        if str(selected_member)=="0":
            default="<option selected value=\"0\">无</option>"
        else:
            default="<option selected value=\"0\">无</option>"
        vm_users=list()
        for user in users:
            tmp_user=VM_ProjectMember(project_id,user,None,None,selected_member)
            vm_users.append(tmp_user)
        pagefileds={"members":vm_users}
        return default+self.get_webpart(pagefileds,ProjectCommonControllPath.member_dropdown_list)
    
    def get_member_dropdown_menu(self,users,project_id,selected_member):
        vm_users=list()
        for user in users:
            tmp_user=VM_ProjectMember(project_id,user,None,None,selected_member)
            vm_users.append(tmp_user)
        pagefileds={"members":vm_users}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.member_dropdown_menu)
    
   
    def get_os_version_dropdown_list(self,field_model,os_value,selected_field_value):
        vm_fields=list()
        for dm_field in field_model.objects.get_by_os(os_value):
            temp_field=VM_IssueField(dm_field,selected_field_value)
            vm_fields.append(temp_field)
        pagefileds={"fields":vm_fields}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.issue_field_dropdown_list)
            
            
        
        
        
        
        
    
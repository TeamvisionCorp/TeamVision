#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.project.pagefactory.project_pageworker import ProjectPageWorker
from teamvision.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from teamvision.project.viewmodels.project_left_nav_bar import ProjectSettingsLeftNavBar
from teamvision.project.viewmodels.project_sub_nav_bar import ProjectSettingsSubNavBar
from teamvision.project.viewmodels.vm_project import VM_Project
from teamvision.project.viewmodels.vm_project_member import VM_ProjectMember
from teamvision.project.viewmodels.vm_project_version import VM_ProjectVersion
from teamvision.project.models import Project,ProjectRole,ProjectMember,Version,ProjectModule
from teamvision.project.viewmodels.vm_member_role import VM_MemberRole
from teamvision.project.pagefactory.project_template_path import ProjectSettingsPath
from django.template import RequestContext
from gatesidelib.common.simplelogger import SimpleLogger
from business.auth_user.user_service import UserService
from business.project.memeber_service import MemberService
from teamvision.auth_extend.user.pagefactory.user_common_pageworker import UserCommonControllPageWorker
from teamvision.project.viewmodels.vm_project_module import VM_ProjectModule


class ProjectSettingsPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.left_nav_bar_model=ProjectSettingsLeftNavBar
        self.subpage_model=ProjectSettingsSubNavBar
    
    def get_full_page(self,request,projectid, sub_nav_action):
        sub_leftnav=self.get_settings_sub_navbar(request,projectid,sub_nav_action)
        left_nav_bar=self.get_settings_left_bar(request,projectid,sub_nav_action)
        project_info=self.get_project_info_webpart(request, projectid, sub_nav_action)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_leftnav':sub_leftnav,'project_info':project_info}
        return self.get_full_page_with_header(request, pagefileds, projectid,'settings/index.html')
    
    
    def get_project_info_webpart(self,request,projectid,sub_nav_action):
        result=""
        if sub_nav_action.upper()=="BASIC":
            result=self.get_settings_project_basic(request,projectid)
            
        if sub_nav_action.upper()=="MEMBER":
            result=self.get_settings_project_member_webpart(request,projectid)
        
        if sub_nav_action.upper()=="VERSION":
            result=self.get_settings_project_version_webpart(projectid)
        
        if sub_nav_action.upper()=="MODULE":
            result=self.get_settings_project_module_webpart(projectid)
        
        if sub_nav_action.upper()=="WEBHOOK":
            result=self.get_settings_project_webhook(request,projectid)
        return result;
        
    
    def get_settings_left_bar(self,request,projectid, sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,projectid,ProjectSettingsPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_settings_sub_navbar(self,request,projectid, sub_nav_action):
        
        return self.get_sub_nav_bar(request, self.subpage_model, projectid,ProjectSettingsPath.sub_nav_template_path,sub_nav_action=sub_nav_action)
    
    
    def get_settings_create_dialog(self,request,projectid):
        form_html=self.get_project_create_form(request,projectid,True)
        context_instance=RequestContext(request)
        pagefileds={'formhtml':form_html,'context_instance':context_instance}
        return self.get_webpart(pagefileds,ProjectSettingsPath.project_create_dialog_path)
    
    def get_project_create_form(self,request,projectid,iscreate):
        result=""
        if projectid:
            dm_project=Project.objects.get(projectid)
        else:
            dm_project=Project()
        page=VM_Project(request.user,iscreate,dm_project,projectid)
        context_instance=RequestContext(request)
        user_common_page_worker=UserCommonControllPageWorker(request)
        project_common_page_worker=ProjectCommonControllPageWorker(request)
        project_lead_controll=user_common_page_worker.get_user_dropdown_list(dm_project.PBLead)
        platform_control=project_common_page_worker.get_platform_dropdown_list(projectid)
        product_controll=project_common_page_worker.get_product_dropdown_list(request.user.id,dm_project.Product)
        pagefileds={'page':page,'context_instance':context_instance,"project_lead_controll":project_lead_controll,"platform_control":platform_control,"product_controll":product_controll}
        result=self.get_webpart(pagefileds,ProjectSettingsPath.project_create_form_path)
        return result
            
            
        
    
    def get_settings_project_basic(self,request,projectid):
        editform=self.get_project_create_form(request, projectid,False)
        dm_project=Project.objects.get(projectid)
        is_creator=dm_project.PBCreator==request.user.id
        context_instance=RequestContext(request)
        pagefileds={'editform':editform,"is_creator":is_creator,'context_instance':context_instance}
        return self.get_webpart(pagefileds,ProjectSettingsPath.project_basic_template_path)
    
    def get_settings_project_member_webpart(self,request,projectid):
        member_menu=self.get_settings_project_member_menu(projectid,request.user,"member")
        members_control=self.get_project_member_list_controll(projectid,request.user)
        pagefileds={"member_menu":member_menu,"member_list":members_control,'project_id':projectid}
        return self.get_webpart(pagefileds,ProjectSettingsPath.project_member_template_path)
    
    
    def get_project_member_add_dialog(self,request,projectid):
        project_common_page_worker=ProjectCommonControllPageWorker(request)
        project_list_controll=project_common_page_worker.get_myproject_dropdown_list(request,0)
        member_users=MemberService.get_member_users(projectid)
        member_user_ids=[user.id for user in member_users]
        not_member_users=UserService.all_users().exclude(id__in=member_user_ids)
        source_user_list=project_common_page_worker.get_user_listbox(not_member_users, projectid)
        member_user_list=project_common_page_worker.get_user_listbox(member_users,projectid)
        pagefileds={"project_list_controll":project_list_controll,"source_user_list":source_user_list,'member_user_list':member_user_list}
        return self.get_webpart(pagefileds,ProjectSettingsPath.project_member_add_dialog)
        
    
    def get_project_member_list_controll(self,projectid,login_user):
        members=self.get_project_members(projectid,login_user)
        pagefileds={"members":members}
        return self.get_webpart(pagefileds,ProjectSettingsPath.project_member_list_path)
    
    def get_settings_project_webhook(self,request,projectid):
        return self.get_webpart_none_args(ProjectSettingsPath.project_webhook_template_path)
    
    def get_settings_project_member_menu(self,projectid,login_user,menu_role):
        users=list()
        for user in UserService.all_users():
            tmp_user=VM_ProjectMember(projectid,user,None,login_user)
            users.append(tmp_user)
        pagefileds={"members":users,"menu_role":menu_role}
        return self.get_webpart(pagefileds, ProjectSettingsPath.project_member_menu_path)
    
    def get_project_members(self,project_id,login_user):
        vm_members=list()
        for user in MemberService.get_member_users(project_id):
            member=ProjectMember.objects.get_members(project_id).filter(PMMember=user.id)
            role_menu=self.get_settings_project_member_role_menu(member[0].PMRoleID, login_user)
            tmp_member=VM_ProjectMember(project_id,user,role_menu,login_user)
            vm_members.append(tmp_member)
        return vm_members 
    
    
    def get_settings_project_member_role_menu(self,member,login_user):
        roles=list()
        for role in ProjectRole.objects.all():
            tmp_role=VM_MemberRole(role,member,login_user)
            roles.append(tmp_role)
        pagefileds={"roles":roles}
        return self.get_webpart(pagefileds,ProjectSettingsPath.project_member_role_menu_path)
  
    
   
    def get_settings_project_version_webpart(self,projectid):
        version_list_controll=self.get_version_list_controll(projectid)
        context_fileds={'version_list_controll':version_list_controll}
        return self.get_webpart(context_fileds,ProjectSettingsPath.version_list_page_path)
    
    def get_version_list_controll(self,projectid):
        versions=self.get_versions(projectid)
        context_fileds={'versions':versions}
        return self.get_webpart(context_fileds,ProjectSettingsPath.version_list_controll_path)
    def get_versions(self,projectid):
        version_list=list()
        for version in Version.objects.all().filter(VProjectID=projectid).order_by("-id"):
            temp_version=VM_ProjectVersion(version)
            version_list.append(temp_version)
        return version_list
    
    def get_settings_project_module_webpart(self,projectid):
        module_list_controll=self.get_module_list_controll(projectid)
        context_fileds={'module_list_controll':module_list_controll}
        return self.get_webpart(context_fileds,ProjectSettingsPath.module_list_page_path)
    
    def get_module_list_controll(self,projectid):
        modules=self.get_modules(projectid)
        context_fileds={'modules':modules}
        return self.get_webpart(context_fileds,ProjectSettingsPath.module_list_controll_path)
    
    def get_modules(self,project_id):
        module_list=list()
        for module in ProjectModule.objects.project_modules(project_id):
            temp_module=VM_ProjectModule(module,0)
            module_list.append(temp_module)
        return module_list
        
    
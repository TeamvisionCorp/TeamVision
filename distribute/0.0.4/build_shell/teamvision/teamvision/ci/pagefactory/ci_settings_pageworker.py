#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.ci.pagefactory.ci_pageworker import CIPageWorker
from teamvision.ci.pagefactory.ci_common_pageworker import CICommonControllPageWorker
from teamvision.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from teamvision.ci.viewmodels.ci_left_nav_bar import CISettingsLeftNavBar
from teamvision.ci.viewmodels.ci_sub_nav_bar import CISettingsSubNavBar
from teamvision.ci.viewmodels.vm_ci_agent import VM_CIAgent
from teamvision.ci.viewmodels.vm_ci_server import VM_CIServer
from teamvision.project.viewmodels.vm_tag import VM_Tag
from teamvision.ci.models import CICredentials,CIServer
from teamvision.project.models import ProjectOS
from teamvision.home.models import Agent
from teamvision.ci.pagefactory.ci_template_path import CISettingsPath
from teamvision.ci.viewmodels.vm_ci_credential import VM_CICredential
from business.ci.ci_agent_service import CIAgentService
from business.ci.ci_credential_service import CICredentialService
from business.ci.ci_deploy_server_service import CIDeployServerService
from business.ci.ci_task_service import CITaskService



class CISettingsPageWorker(CIPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        CIPageWorker.__init__(self, request)
        self.pagemodel = CISettingsLeftNavBar
        self.subpage_model = CISettingsSubNavBar
    
    def get_ci_settings_global_fullpage(self, request,sub_nav_action):
        left_nav_bar = self.get_settings_left_bar(request)
        sub_nav_bar = self.get_settings_sub_navbar(request,sub_nav_action)
        ci_settings_global_config =self.get_ci_global_config_webpart(request)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_settings_global_config":ci_settings_global_config}
        return self.get_page(page_fileds,CISettingsPath.settings_index_path,request)
    
    def get_ci_settings_agent_fullpage(self, request,sub_nav_action):
        left_nav_bar = self.get_settings_left_bar(request)
        sub_nav_bar = self.get_settings_sub_navbar(request,sub_nav_action)
        ci_settings_agent =self.get_ci_settings_agent_webpart(request)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_settings_agent":ci_settings_agent}
        return self.get_page(page_fileds,CISettingsPath.settings_index_path, request)
    
    def get_ci_settings_tag_fullpage(self, request,sub_nav_action):
        left_nav_bar = self.get_settings_left_bar(request)
        sub_nav_bar = self.get_settings_sub_navbar(request,sub_nav_action)
        ci_settings_tag =self.get_ci_settings_tag_webpart(request)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_settings_tag":ci_settings_tag}
        return self.get_page(page_fileds,CISettingsPath.settings_index_path, request)
       
    def get_ci_settings_credentials_fullpage(self, request,sub_nav_action,credential_id):
        left_nav_bar = self.get_settings_left_bar(request)
        sub_nav_bar = self.get_settings_sub_navbar(request,sub_nav_action)
        ci_settings_credential =self.get_ci_settings_credentials_webpart(request,int(credential_id))
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_settings_credential":ci_settings_credential}
        return self.get_page(page_fileds,CISettingsPath.settings_index_path, request)
    
    
    
    def get_ci_settings_credentials_webpart(self,request,credential_id):
        ci_credentials_list=CICredentialService.get_all_credentials(request)
        vm_credential_list=list()
        for credential in ci_credentials_list:
            temp=VM_CICredential(credential,True,0)
            vm_credential_list.append(temp)

        credentials_form=self.get_ci_settings_credentials_form_webpart(request,credential_id)
        page_fileds = {"ci_credentials_form":credentials_form,"ci_credentials":vm_credential_list,"is_create":credential_id==0}
        return self.get_webpart(page_fileds,CISettingsPath.settings_credential_page)
    
    def get_ci_settings_credentials_form_webpart(self,request,credential_id):
        if credential_id==0:
            temp_credentials=CICredentials()
            vm_credential=VM_CICredential(temp_credentials,True,credential_id)
        else:
            temp_credentials=CICredentials.objects.get(credential_id)
            vm_credential=VM_CICredential(temp_credentials,False,0)
        ci_credential_type=CICommonControllPageWorker.get_credential_type_dropdown_list(self,temp_credentials.CredentialType)
        page_fileds = {"ci_credential":vm_credential,"ci_credential_type":ci_credential_type}
        return self.get_webpart(page_fileds,CISettingsPath.settings_credential_form)
    
    
    def get_ci_settings_agent_webpart(self,request):
        ci_agent_listcontroll=self.get_ci_agent_list_controll_webpart(request)
        page_fileds = {"ci_agent_listcontroll":ci_agent_listcontroll}
        return self.get_webpart(page_fileds,CISettingsPath.settings_agent_webpart)
    
    def get_ci_agent_list_controll_webpart(self,request):
        all_agent=CIAgentService.get_all_agents()
        vm_agents=list()
        for dm_agent in all_agent:
            tmp_agent=VM_CIAgent(dm_agent,0)
            vm_agents.append(tmp_agent)
        page_fileds = {"ci_agents":vm_agents}
        return self.get_webpart(page_fileds,CISettingsPath.settings_agent_controll)
    
    def get_ci_settings_agent_create_form(self,agent_id):
        if str(agent_id)=="0":
            temp_agent=Agent()
            vm_agent=VM_CIAgent(temp_agent,agent_id)
        else:
            temp_agent=Agent.objects.get(agent_id)
            vm_agent=VM_CIAgent(temp_agent,agent_id)
        os_dropdown_list=ProjectCommonControllPageWorker.get_issue_field_dropdown_list(self,ProjectOS,temp_agent.OS)
        agent_tag_list=CICommonControllPageWorker.get_agent_filter_dropdown_list(self,temp_agent.AgentTags)
        page_fileds = {"agent":vm_agent,'os_dropdown_list':os_dropdown_list,'agent_tag_list':agent_tag_list}
        return self.get_webpart(page_fileds,CISettingsPath.settings_agent_create_form)
    
    def get_ci_settings_agent_create_dialog(self,agent_id):
        agent_create_form=self.get_ci_settings_agent_create_form(agent_id)
        page_fileds = {"agent_create_form":agent_create_form,'agent_id':agent_id}
        return self.get_webpart(page_fileds,CISettingsPath.settings_agent_create_dialog)
    
    def get_ci_settings_server_fullpage(self, request,sub_nav_action,server_id):
        left_nav_bar = self.get_settings_left_bar(request)
        sub_nav_bar = self.get_settings_sub_navbar(request,sub_nav_action)
        ci_settings_server =self.get_ci_settings_servers_webpart(request,int(server_id))
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_settings_server":ci_settings_server}
        return self.get_page(page_fileds,CISettingsPath.settings_index_path, request)
    
    
    
    def get_ci_settings_servers_webpart(self,request,server_id):
        ci_servers_list=CIDeployServerService.get_all_servers(request)
        vm_server_list=list()
        for server in ci_servers_list:
            temp=VM_CIServer(server,True,0)
            vm_server_list.append(temp)

        servers_form=self.get_ci_settings_servers_form_webpart(request,server_id)
        page_fileds = {"ci_server_form":servers_form,"ci_servers":vm_server_list,"is_create":server_id==0}
        return self.get_webpart(page_fileds,CISettingsPath.settings_server_page)
    
    def get_ci_settings_servers_form_webpart(self,request,server_id):
        if server_id==0:
            temp_server=CIServer()
            vm_server=VM_CIServer(temp_server,True,server_id)
        else:
            temp_server=CIServer.objects.get(server_id)
            vm_server=VM_CIServer(temp_server,False,0)
        ci_server_credential=CICommonControllPageWorker.get_credential_dropdown_list(self,request,temp_server.Credential)
        page_fileds = {"ci_server":vm_server,"ci_server_credential":ci_server_credential}
        return self.get_webpart(page_fileds,CISettingsPath.settings_server_form)
    
    def get_ci_settings_tag_webpart(self,request):
        ci_tag_list=self.get_ci_tag_list(request)
        page_fileds = {"ci_tag_list":ci_tag_list}
        return self.get_webpart(page_fileds,CISettingsPath.settings_tag_webpart)
    
    def get_ci_tag_list(self,request):
        all_tags=CITaskService.get_avalible_menu_tags(4)
        vm_tags=list()
        for dm_tag in all_tags:
            tmp_tag=VM_Tag(dm_tag,0)
            vm_tags.append(tmp_tag)
        page_fileds = {"ci_tags":vm_tags}
        return self.get_webpart(page_fileds,CISettingsPath.settings_tag_list)
    
    
    
    def get_ci_global_config_webpart(self,request):
        return self.get_webpart_none_args(CISettingsPath.settings_global_config_page_path)
    
    
    def get_settings_left_bar(self, request):
        return self.get_left_nav_bar(request, self.pagemodel, CISettingsPath.left_nav_template_path)
    
    def get_settings_sub_navbar(self, request,sub_nav_action):
        return self.get_sub_nav_bar(request, self.subpage_model, CISettingsPath.sub_nav_template_path, sub_nav_action=sub_nav_action)


        
    

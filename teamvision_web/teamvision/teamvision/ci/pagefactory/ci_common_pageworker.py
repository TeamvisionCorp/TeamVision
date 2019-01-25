#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.ci.pagefactory.ci_pageworker import CIPageWorker
from teamvision.ci.pagefactory.ci_template_path import CICommonControllPath

from business.ci.ci_task_service import CITaskService
from business.ci.ci_agent_service import CIAgentService
from teamvision.project.viewmodels.vm_tag import VM_Tag
from teamvision.ci.viewmodels.vm_ci_agent import VM_CIAgent
from teamvision.ci.models import CIDeployService,CIServer,CaseTag
from teamvision.ci.viewmodels.vm_ci_deploy_service import VM_CIDeployService
from teamvision.ci.viewmodels.vm_data_value import VM_DataValue
from teamvision.ci.viewmodels.vm_ci_credential import VM_CICredential
from teamvision.ci.viewmodels.vm_ci_server import VM_CIServer
from teamvision.ci.viewmodels.vm_ci_casetag import VM_CICaseTag
from business.ci.ci_credential_service import CICredentialService
from business.common.system_config_service import SystemConfigService
from business.ci.ci_task_parameter_service import CITaskParameterService

class CICommonControllPageWorker(CIPageWorker):
    '''
    项目页面生成
    '''
    
    def __init__(self, request):
        '''
        Constructor
        '''
        CIPageWorker.__init__(self, request)
    
    def get_deploy_service_dropdown_list(self, selected_service_id):
        vm_deploy_services = list()
        for dm_service in CIDeployService.objects.all():
            tem_service = VM_CIDeployService(dm_service, selected_service_id)
            vm_deploy_services.append(tem_service)
        pagefileds = {"deploy_services":vm_deploy_services}
        return self.get_webpart(pagefileds, CICommonControllPath.service_dropdown_controll)
    
    def get_deploy_server_dropdown_list(self, selected_server_id):
        vm_deploy_servers = list()
        for dm_server in CIServer.objects.all():
            tem_server = VM_CIServer(dm_server,False,selected_server_id)
            vm_deploy_servers.append(tem_server)
        pagefileds = {"deploy_servers":vm_deploy_servers}
        return self.get_webpart(pagefileds, CICommonControllPath.ci_deploy_server_dropdownlist)
    
    def get_agent_filter_dropdown_list(self, condations_list):
        vm_agent_filter_tags = list()
        for dm_tag in CITaskService.get_agent_filter__tags():
            tem_tag = VM_Tag(dm_tag, condations_list)
            vm_agent_filter_tags.append(tem_tag)
        pagefileds = {"filter_condations":vm_agent_filter_tags}
        return self.get_webpart(pagefileds, CICommonControllPath.agent_condations_controll)
    
    def get_agent_asgin_dropdown_list(self, selected_agent_id):
        vm_agent = list()
        for dm_agent in CIAgentService.get_all_agents():
            tem_agent = VM_CIAgent(dm_agent, selected_agent_id)
            vm_agent.append(tem_agent)
        pagefileds = {"agent_list":vm_agent}
        return self.get_webpart(pagefileds, CICommonControllPath.agent_controll)
    
    def my_ci_task_dropdown_list(self):
        my_ci_task_lists=CITaskService.get_product_ci_tasks(self.request,0,'ALL')
        pagefileds = {"all_tasks":my_ci_task_lists}
        return self.get_webpart(pagefileds, CICommonControllPath.ci_task_dropdownlist)
    
    def task_parameter_dropdown_list(self,task_id):
        task_parameter_groups=CITaskParameterService.task_parameter_list(int(task_id))
        pagefileds = {"ci_task_parameter_groups":task_parameter_groups}
        return self.get_webpart(pagefileds,CICommonControllPath.task_parameter_dropdownlist)
    
    def get_credential_type_dropdown_list(self, selected_credential_id):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.get_credential_type():
            tem_data = VM_DataValue(dm_data_value, selected_credential_id)
            vm_data_values.append(tem_data)
        pagefileds = {"credentials":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.credential_type_dropdownlist_controll)
    
    def get_credential_dropdown_list(self,request,selected_credential_id):
        vm_credentials = list()
        for dm_ci_credential in CICredentialService.get_all_credentials(request):
            tem_credential = VM_CICredential(dm_ci_credential,False,selected_credential_id)
            vm_credentials.append(tem_credential)
        pagefileds = {"credentials":vm_credentials}
        return self.get_webpart(pagefileds, CICommonControllPath.credential_dropdown_controll)
    
    def get_git_checkut_strategy_dropdown_list(self, selected_strategy_id):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.get_git_strategy_type():
            tem_data = VM_DataValue(dm_data_value, selected_strategy_id)
            vm_data_values.append(tem_data)
        pagefileds = {"checkout_strategies":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.git_checkout_strategy)
    
    def get_svn_checkut_strategy_dropdown_list(self, selected_strategy_id):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.get_svn_strategy_type():
            tem_data = VM_DataValue(dm_data_value, selected_strategy_id)
            vm_data_values.append(tem_data)
        pagefileds = {"checkout_strategies":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.svn_checkout_strategy)
    
    def get_jdk_buildtools_dropdown_list(self, selected_text):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.get_jdk_build_tools():
            tem_data = VM_DataValue(dm_data_value,0,selected_text)
            vm_data_values.append(tem_data)
        pagefileds = {"build_tools":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.build_tool_sdk)
    
    def host_env_dropdown_list(self, selected_text):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.test_env():
            tem_data = VM_DataValue(dm_data_value,selected_text)
            vm_data_values.append(tem_data)
        pagefileds = {"build_tools":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.build_tool_testenv)

    
    def get_gradle_buildtools_dropdown_list(self, selected_text):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.get_gradle_build_tools():
            tem_data = VM_DataValue(dm_data_value,0,selected_text)
            vm_data_values.append(tem_data)
        pagefileds = {"build_tools":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.build_tool_gradle)
    
    def get_xcode_buildtools_dropdown_list(self, selected_text):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.get_xcode_build_tools():
            tem_data = VM_DataValue(dm_data_value,0,selected_text)
            vm_data_values.append(tem_data)
        pagefileds = {"build_tools":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.build_tool_gradle)
    
    def get_pods_buildtools_dropdown_list(self, select_value):
        vm_data_values = list()
        for dm_data_value in SystemConfigService.get_pods_build_tools():
            tem_data = VM_DataValue(dm_data_value,select_value)
            vm_data_values.append(tem_data)
        pagefileds = {"build_tools":vm_data_values}
        return self.get_webpart(pagefileds, CICommonControllPath.build_tool_pods)
    
    def get_casetag_dropdown_list(self, select_value):
        vm_case_taglist = list()
        if select_value=="":
            select_value="1,"
        for case_tag in CaseTag.objects.all():
            tem_data = VM_CICaseTag(case_tag,select_value)
            vm_case_taglist.append(tem_data)
        pagefileds = {"case_tags":vm_case_taglist}
        print(self.get_webpart(pagefileds, CICommonControllPath.case_tag_dropdownlist))
        return self.get_webpart(pagefileds, CICommonControllPath.case_tag_dropdownlist)
    
    def get_ci_task_tag_menu(self):
        ci_tags = list()
        for dm_tag in CITaskService.get_avalible_menu_tags(1):
            tem_tag = VM_Tag(dm_tag,'0,0')
            ci_tags.append(tem_tag)
        pagefileds = {"ci_tags":ci_tags}
        return self.get_webpart(pagefileds, CICommonControllPath.task_tag_filter_menu)
        
        
        
        
        
        
    

# coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.ci.pagefactory.ci_pageworker import CIPageWorker
from doraemon.ci.pagefactory.ci_template_path import CIPluginPath

from doraemon.ci.pagefactory.ci_common_pageworker import CICommonControllPageWorker
from doraemon.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from doraemon.ci.models import CITask, CIDeployService
from doraemon.ci.viewmodels.plugins.vm_ci_scm_git import VM_GitPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_scm_svn import VM_SvnPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_shell_command import VM_ShellCommandPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_shell_build import VM_ShellCommandBuildPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_gradle_build import VM_GradleBuildPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_ant_build import VM_AntBuildPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_ios_build import VM_IOSBuildPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_ios_command_build import VM_IOSCommandBuildPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_service_replace import VM_ServiceReplacePlugin
from doraemon.ci.viewmodels.plugins.vm_ci_deploy_service import VM_DeployServicePlugin
from doraemon.ci.viewmodels.plugins.vm_ci_copy_file2server import VM_Copy2ServerPlugin
from doraemon.ci.viewmodels.plugins.vm_auto_apitesting import VM_AutoAPITestingPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_xcode_settings_check import VM_XCodeSettingCheckPlugin
from doraemon.ci.viewmodels.plugins.vm_ci_xctest import VM_XCTestPlugin
from doraemon.ci.viewmodels.plugins.vm_auto_webui_testing import VM_AutoWebUITestingPlugin


class CIPluginPageWorker(CIPageWorker):
    '''
    项目页面生成
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        CIPageWorker.__init__(self, request)

    def get_plugin(self, plugin_dict, plugin_id, task_id=0):
        result = None
        if VM_GitPlugin.plugin_id == plugin_id:
            result = self.get_git_plugin(self.request, plugin_dict)

        if VM_SvnPlugin.plugin_id == plugin_id:
            result = self.get_svn_plugin(self.request, plugin_dict)

        if VM_ShellCommandPlugin.plugin_id == plugin_id:
            result = self.get_shell_command_plugin(plugin_dict)

        if VM_ShellCommandBuildPlugin.plugin_id == plugin_id:
            result = self.get_shell_command_build_plugin(plugin_dict)

        if VM_GradleBuildPlugin.plugin_id == plugin_id:
            result = self.get_gradle_build_plugin(self.request, plugin_dict)

        if VM_AntBuildPlugin.plugin_id == plugin_id:
            result = self.get_ant_build_plugin(self.request, plugin_dict)

        if VM_IOSBuildPlugin.plugin_id == plugin_id:
            result = self.get_ios_build_plugin(self.request, plugin_dict)

        if VM_ServiceReplacePlugin.plugin_id == plugin_id:
            result = self.get_service_replace_plugin(self.request, plugin_dict, task_id)

        if VM_DeployServicePlugin.plugin_id == plugin_id:
            result = self.get_deploy_service_plugin(self.request, plugin_dict, task_id)

        if VM_IOSCommandBuildPlugin.plugin_id == plugin_id:
            result = self.get_ios_command_build_plugin(self.request, plugin_dict)

        if VM_Copy2ServerPlugin.plugin_id == plugin_id:
            result = self.copy2_server_plugin(self.request, plugin_dict, task_id)

        if VM_AutoAPITestingPlugin.plugin_id == plugin_id:
            result = self.auto_apitesting_plugin(self.request, plugin_dict)

        if VM_AutoWebUITestingPlugin.plugin_id == plugin_id:
            result = self.auto_webuitesting_plugin(self.request, plugin_dict)

        if VM_XCodeSettingCheckPlugin.plugin_id == plugin_id:
            result = self.xcode_settings_check_plugin(self.request, plugin_dict)

        if VM_XCTestPlugin.plugin_id == plugin_id:
            result = self.get_xctest_plugin(plugin_dict)

        return result

    def get_git_plugin(self, request, plugin_dict):
        vm_plugin = VM_GitPlugin(plugin_dict)
        ci_credentials_list = CICommonControllPageWorker.get_credential_dropdown_list(self, request,
                                                                                      vm_plugin.ci_credentials)
        git_check_out_strategy = CICommonControllPageWorker.get_git_checkut_strategy_dropdown_list(self,
                                                                                                   vm_plugin.git_check_out_strategy)
        pagefileds = {'plugin': vm_plugin, "ci_credentials_list": ci_credentials_list}
        pagefileds['git_check_out_strategy'] = git_check_out_strategy
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_gradle_build_plugin(self, request, plugin_dict):
        vm_plugin = VM_GradleBuildPlugin(plugin_dict)
        build_tool_jdk = CICommonControllPageWorker.get_jdk_buildtools_dropdown_list(self, vm_plugin.build_tool_jdk)
        build_tool_gradle = CICommonControllPageWorker.get_gradle_buildtools_dropdown_list(self,
                                                                                           vm_plugin.build_tool_gradle)
        pagefileds = {'plugin': vm_plugin, "build_tool_jdk": build_tool_jdk}
        pagefileds['build_tool_gradle'] = build_tool_gradle
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_ant_build_plugin(self, request, plugin_dict):
        vm_plugin = VM_AntBuildPlugin(plugin_dict)
        build_tool_jdk = CICommonControllPageWorker.get_jdk_buildtools_dropdown_list(self, vm_plugin.build_tool_jdk)
        pagefileds = {'plugin': vm_plugin, "build_tool_jdk": build_tool_jdk}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def auto_apitesting_plugin(self, request, plugin_dict):
        vm_plugin = VM_AutoAPITestingPlugin(plugin_dict)
        print(plugin_dict)
        auto_tool_jdk = CICommonControllPageWorker.get_jdk_buildtools_dropdown_list(self, vm_plugin.auto_tool_jdk)
        auto_host_info = CICommonControllPageWorker.host_env_dropdown_list(self, vm_plugin.auto_host_info)
        case_tag_list = CICommonControllPageWorker.get_casetag_dropdown_list(self, vm_plugin.case_filters)
        pagefileds = {'plugin': vm_plugin, "auto_tool_jdk": auto_tool_jdk, "auto_host_info": auto_host_info,
                      'case_tag_list': case_tag_list}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def auto_webuitesting_plugin(self, request, plugin_dict):
        vm_plugin = VM_AutoWebUITestingPlugin(plugin_dict)
        print(plugin_dict)
        auto_tool_jdk = CICommonControllPageWorker.get_jdk_buildtools_dropdown_list(self, vm_plugin.auto_tool_jdk)
        auto_host_info = CICommonControllPageWorker.host_env_dropdown_list(self, vm_plugin.auto_host_info)
        case_tag_list = CICommonControllPageWorker.get_casetag_dropdown_list(self, vm_plugin.case_filters)
        pagefileds = {'plugin': vm_plugin, "auto_tool_jdk": auto_tool_jdk, "auto_host_info": auto_host_info,
                      'case_tag_list': case_tag_list}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def xcode_settings_check_plugin(self, request, plugin_dict):
        vm_plugin = VM_XCodeSettingCheckPlugin(plugin_dict)
        pagefileds = {'plugin': vm_plugin}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_svn_plugin(self, request, plugin_dict):
        vm_plugin = VM_SvnPlugin(plugin_dict)
        ci_credentials_list = CICommonControllPageWorker.get_credential_dropdown_list(self, request,
                                                                                      vm_plugin.ci_credentials)
        svn_check_out_strategy = CICommonControllPageWorker.get_svn_checkut_strategy_dropdown_list(self,
                                                                                                   vm_plugin.svn_check_out_strategy)
        pagefileds = {'plugin': vm_plugin, "ci_credentials_list": ci_credentials_list}
        pagefileds['svn_check_out_strategy'] = svn_check_out_strategy
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_ios_build_plugin(self, request, plugin_dict):
        vm_plugin = VM_IOSBuildPlugin(plugin_dict)
        build_tool_xcode = CICommonControllPageWorker.get_xcode_buildtools_dropdown_list(self,
                                                                                         vm_plugin.build_tool_xcode)
        build_tool_pods = CICommonControllPageWorker.get_pods_buildtools_dropdown_list(self, vm_plugin.build_tool_pods)
        pagefileds = {'plugin': vm_plugin, "build_tool_xcode": build_tool_xcode, "build_tool_pods": build_tool_pods}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_ios_command_build_plugin(self, request, plugin_dict):
        vm_plugin = VM_IOSCommandBuildPlugin(plugin_dict)
        build_tool_xcode = CICommonControllPageWorker.get_xcode_buildtools_dropdown_list(self,
                                                                                         vm_plugin.build_tool_xcode)
        pagefileds = {'plugin': vm_plugin, "build_tool_xcode": build_tool_xcode}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_service_replace_plugin(self, request, plugin_dict, task_id):
        replace_config = self.get_service_replace_config(request, task_id)
        vm_plugin = VM_ServiceReplacePlugin(replace_config, plugin_dict)
        deploy_servers = CICommonControllPageWorker.get_deploy_server_dropdown_list(self, vm_plugin.deploy_server)
        pagefileds = {'plugin': vm_plugin, "deploy_servers": deploy_servers}

        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_service_replace_config(self, request, task_id):
        if not task_id:
            task_id = int(request.GET.get("task_id", 0))
        ci_task = CITask.objects.get(task_id)
        if ci_task.DeployService:
            deploy_service = CIDeployService.objects.get(ci_task.DeployService)
        return deploy_service.AdvanceConfig

    def get_deploy_service_plugin(self, request, plugin_dict, task_id):
        # replace_config=self.get_service_replace_config(request,task_id)
        vm_plugin = VM_DeployServicePlugin(None, plugin_dict)
        deploy_servers = CICommonControllPageWorker.get_deploy_server_dropdown_list(self, vm_plugin.deploy_server)
        deploy_services = CICommonControllPageWorker.get_deploy_service_dropdown_list(self, vm_plugin.deploy_service)
        pagefileds = {'plugin': vm_plugin, "deploy_servers": deploy_servers, 'deploy_services': deploy_services}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def copy2_server_plugin(self, request, plugin_dict, task_id):
        vm_plugin = VM_Copy2ServerPlugin(plugin_dict)
        deploy_servers = CICommonControllPageWorker.get_deploy_server_dropdown_list(self, vm_plugin.deploy_server)
        pagefileds = {"deploy_servers": deploy_servers, 'plugin': vm_plugin}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_shell_command_plugin(self, plugin_dict):
        vm_plugin = VM_ShellCommandPlugin(plugin_dict)
        pagefileds = {'plugin': vm_plugin}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_shell_command_build_plugin(self, plugin_dict):
        vm_plugin = VM_ShellCommandBuildPlugin(plugin_dict)
        pagefileds = {'plugin': vm_plugin}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

    def get_xctest_plugin(self, plugin_dict):
        vm_plugin = VM_XCTestPlugin(plugin_dict)
        pagefileds = {'plugin': vm_plugin}
        return self.get_webpart(pagefileds, vm_plugin.get_template_path())

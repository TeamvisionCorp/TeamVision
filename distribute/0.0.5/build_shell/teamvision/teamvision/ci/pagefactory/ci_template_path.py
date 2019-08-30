#coding=utf-8
'''
Created on 2015-10-10

@author: Devuser
'''

class CITemplatePath(object):
    left_nav_template_path = "ci/ci_left_nav.html"
    



class CIDashBoardPath(CITemplatePath):
    dashboard_index_path = "dashboard/ci_dashboard_index.html"
    task_queue_webpart="dashboard/ci_dashboard_task_queue.html"
    task_queue_list_controll="dashboard/ci_dashboard_task_queue_list_controll.html"
    task_build_status_controll="dashboard/ci_dashboard_build_status_controll.html"
    task_build_status_page="dashboard/ci_dashboard_build_status_page.html"
    


class CITaskPath(CITemplatePath):
    task_index_path = "task/ci_task_index.html"
    sub_nav_template_path = "task/ci_task_leftsub_nav.html"
    task_create_dialog = "task/ci_task_create_dialog.html"
    task_list_webpart = "task/ci_task_list_page.html"
    task_list_controll = "task/ci_task_list_controll.html"
    task_config_webpart = "task/ci_task_config_page.html"
    task_config_basic = "task/ci_task_config_basic.html"
    task_create_form = "task/ci_task_create_form.html"
    task_config_pop_menu = "task/ci_task_plugin_menu_control.html"
    task_history_list="task_history/ci_task_history_list_controll.html"
    task_history_page="task_history/ci_task_history_list_page.html"
    task_download_package="task_history/ci_task_package_download__control.html"
    history_build_log="task_history/ci_task_build_log.html"
    task_property_nav= "task/ci_task_property_nav.html"
    testing_property_nav= "testing_task/testing_task_property_nav.html"
    task_parameter_list="task_parameter/task_parameter_list_controll.html"
    task_parameter_page="task_parameter/task_parameter_list_page.html"
    task_parameter_edit="task_parameter/task_parameter_edit_page.html"
    task_parameter_menu="task_parameter/task_parameter_menu_control.html"
    task_build_confirm_page="task/ci_task_build_confirm_page.html"
    task_parameter_confirm="task_parameter/task_release_parameter_group__confirm_dialog.html"
    task_parameter_group_type_menu="task_parameter/task_parameter_group_type_menu.html"
    task_parameter_plugin="task_parameter/task_plugin.html"
    task_changelog_list="task_change_log/task_change_log_list.html"
    task_changelog_page="task_change_log/task_change_log_page.html"
    task_changelog_detail="task_change_log/task_changelog_detail_page.html"
    history_clean_page="task_history/ci_task_history_clean_page.html"
    task_confirm_dialog="task/ci_task_confirm_dialog.html"
    

class TestingTaskPath(CITemplatePath):
    testing_history_list="testing_task/testing_history_list_controll.html"
    teting_history_page="testing_task/testing_history_list_page.html"
    teting_analytics_webpart="testing_task/testing_history_analytics.html"
    teting_caseresult_list="testing_task/testing_case_result_list_controll.html"



    
class CIServicePath(CITemplatePath):
    service_index_path = "service/ci_service_index.html"
    sub_nav_template_path = "service/ci_service_leftsub_nav.html"
    service_list_webpart = "service/ci_service_list_page.html"
    service_list_controll = "service/ci_service_list_controll.html"
    service_config_page="service/ci_service_config_page.html"
    
    
    
class CISettingsPath(CITemplatePath):
    settings_index_path = "settings/ci_settings_index.html"
    sub_nav_template_path = "settings/ci_settings_leftsub_nav.html"
    settings_global_config_page_path="settings/ci_settings_global_variable_page.html"
    settings_agent_controll="settings/ci_settings_agent_list_controll.html"
    settings_agent_create_form="settings/ci_agent_create_form.html"
    settings_agent_create_dialog="settings/ci_settings_agent_create_dialog.html"
    settings_agent_webpart="settings/ci_settings_agent_page.html"
    settings_server_form="settings/ci_settings_server_form.html"
    settings_server_page="settings/ci_settings_server_page.html"
    settings_credential_form="settings/ci_settings_credential_form.html"
    settings_credential_page="settings/ci_settings_credential_page.html"
    settings_tag_list="settings/ci_settings_tag_list_controll.html"
    settings_tag_webpart="settings/ci_settings_tag_listpage.html"
    


class CIPluginPath(object):
    svn_plugin = "plugins/ci_svn_plugin.html"
    git_plugin = "plugins/ci_git_plugin.html"
    shell_command="plugins/ci_shell_command_plugin.html"
    shell_build="plugins/ci_shell_build_plugin.html"
    gradle_build="plugins/ci_gradle_build_plugin.html"
    ant_build="plugins/ci_ant_build_plugin.html"
    ios_build="plugins/ci_ios_build_plugin.html"
    ios_command_build="plugins/ci_ios_command_build_plugin.html"
    service_replace_file="plugins/ci_service_replace_plugin.html"
    service_deploy="plugins/ci_deploy_service_plugin.html"
    copy2_server="plugins/ci_copy_2server_plugin.html"
    auto_apitesting="plugins/auto_apitesting_plugin.html"
    auto_webuitesting="plugins/auto_webui_testing_plugin.html"
    xcode_settings_check="plugins/ci_xcode_settings_check_plugin.html"
    xctest_plugin="plugins/ci_xctest_plugin.html"

    
class CICommonControllPath(object):
    service_dropdown_controll = "common/deploy_service_dropdown_list_controll.html"
    agent_condations_controll = "common/agent_condations_dropdown_list_controll.html"
    agent_controll = "common/agent_dropdown_list_controll.html"
    credential_type_dropdownlist_controll="common/credential_type_dropdown_list_controll.html"
    credential_dropdown_controll="common/server_credential_dropdown_list_controll.html"
    ci_build_log_js="common/ci_build_log.js"
    ci_build_log_dialog="common/ci_build_log_dialog.html"
    svn_checkout_strategy="common/svn_checkout_strategy_dropdown_list_controll.html"
    git_checkout_strategy="common/git_checkout_strategy_dropdown_list_controll.html"
    build_tool_sdk="common/buildtools_jdk_dropdown_list_controll.html"
    build_tool_testenv="common/buildtools_testenv_dropdown_list_controll.html"
    build_tool_gradle="common/buildtools_gradle_dropdown_list_controll.html"
    build_tool_xcode="common/buildtools_xcode_dropdown_list_controll.html"
    build_tool_pods="common/buildtools_pods_dropdown_list_controll.html"
    ci_deploy_server_dropdownlist="common/deploy_server_dropdown_list_controll.html"
    ci_task_dropdownlist="common/ci_task_dropdown_list_controll.html"
    task_parameter_dropdownlist="common/build_parameter_dropdown_list_controll.html"
    case_tag_dropdownlist="common/casetag_dropdown_list_controll.html"
    task_tag_filter_menu="common/task_tag_filter_menu_control.html"
    project_filter_menu="common/task_project_filter_menu.html"
    
    

    
    

    
    
    

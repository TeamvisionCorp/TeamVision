#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.ci.pagefactory.ci_pageworker import CIPageWorker

from doraemon.ci.viewmodels.vm_ci_task import VM_CITask
from doraemon.ci.pagefactory.ci_template_path import CITaskPath,CICommonControllPath
from doraemon.ci.pagefactory.ci_common_pageworker import CICommonControllPageWorker
from doraemon.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from doraemon.project.pagefactory.project_template_path import ProjectCommonControllPath
from doraemon.ci.models import CITaskPlugin, CITask,CITaskHistory
from doraemon.ci.pagefactory.ci_section_pageworker import CISectionPageWorker
from json.decoder import JSONDecoder
from doraemon.ci.viewmodels.vm_ci_task_changelog import VM_CITaskChangeLog
from doraemon.project.models import Tag
from doraemon.project.viewmodels.vm_tag import VM_Tag
from doraemon.ci.viewmodels.vm_ci_task_history import VM_CITaskHistory
from doraemon.ci.viewmodels.vm_task_parameter_group_diff import VM_TaskParameterGroupDiff
from doraemon.ci.viewmodels.vm_task_parameter_group import VM_TaskParameterGroup
from doraemon.project.pagefactory.project_template_path import ProjectTaskPath
from business.ci.ci_task_service import CITaskService
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_history_service import CITaskHistoryService
from doraemon.project.pagefactory.project_pageworker import ProjectPageWorker
from doraemon.ci.viewmodels.vm_ci_task_config import VM_CITaskConfig
from doraemon.ci.pagefactory import ci_common_pageworker



class CITaskPageWorker(CIPageWorker):
    '''
    项目页面生成器
    '''
   
    def __init__(self, request):
        '''
        Constructor
        '''
        CIPageWorker.__init__(self, request)
    
    def get_ci_task_fullpage(self, request, task_type, sub_nav_action):
        dm_products = CITaskService.get_products_include_me(request)
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request, dm_products, sub_nav_action)
        ci_task_webpart = self.get_ci_task_list_webpart(request, task_type, sub_nav_action,"所有任务")
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_task_list":ci_task_webpart}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    
    def get_ci_task_config_page(self, request,task_id,task_property):
        dm_products = CITaskService.get_products_include_me(request)
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request, dm_products, 0,task_id,task_property)
        ci_task_config_webpart = self.get_task_config_webpart(request, task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_task_config":ci_task_config_webpart}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    
    def get_ci_task_create_dialog(self, request):
        create_form_webpart = self.get_task_create_form(request)
        pagefileds = {"task_create_form":create_form_webpart}
        return self.get_webpart(pagefileds, CITaskPath.task_create_dialog)
    
    def get_ci_task_config_basic(self, request, task_id):
        dm_ci_task = CITask.objects.get(task_id)
        vm_ci_task = VM_CITask(dm_ci_task, None, False,True)
        common_page_worker = CICommonControllPageWorker(request)
        deploy_services = common_page_worker.get_deploy_service_dropdown_list(dm_ci_task.DeployService)
        my_projects = ProjectCommonControllPageWorker.get_myproject_dropdown_list(self,request, dm_ci_task.Project)
        ci_agent_list=CICommonControllPageWorker.get_agent_asgin_dropdown_list(self,vm_ci_task.task_config.get_basic_section().get_asgin_agent())
        ci_agent_filter_condations = CICommonControllPageWorker.get_agent_filter_dropdown_list(self,vm_ci_task.task_config.get_basic_section().get_agent_filter_condations())
        case_tag_list=CICommonControllPageWorker.get_casetag_dropdown_list(self, vm_ci_task.task_config.get_basic_section().get_case_filters())
        pagefileds = {"ci_task_project":my_projects, "task":vm_ci_task, "ci_deploy_services":deploy_services}
        pagefileds["ci_agent_filter_condations"] = ci_agent_filter_condations
        pagefileds['basic_section'] = vm_ci_task.task_config.get_basic_section()
        pagefileds['ci_agent_list']=ci_agent_list
        pagefileds['case_tag_list']=case_tag_list
        return self.get_webpart(pagefileds, CITaskPath.task_config_basic)
    
    def get_ci_task_confirm_dialog(self):
        return self.get_webpart_none_args(CITaskPath.task_confirm_dialog)
    
    
    
    def get_dashboard_task_list_webpart(self, request):
        dm_ci_tasks = CITaskService.get_my_ci_tasks(request,0,"all")
        task_list_controll = self.get_ci_task_list_controll(request,dm_ci_tasks,False)
        project_pageworker=ProjectPageWorker(request)
        project_filter=project_pageworker.get_project_menu(request,CICommonControllPath.project_filter_menu)
        ci_common_pageworker=CICommonControllPageWorker(request)
        task_tag_filter=ci_common_pageworker.get_ci_task_tag_menu()
        pagefileds = {"ci_task_listcontroll":task_list_controll,"project_filter":project_filter,"ci_task_page_title":"dashboard"}
        pagefileds['task_tag_filter']=task_tag_filter
        return self.get_webpart(pagefileds, CITaskPath.task_list_webpart)
    
    def dashboard_more_task_list(self,request):
#         page_size=int(request.POST.get("page_size",0))
#         start_index=int((page_size/9)*9)
#         end_index=int(((page_size/9)+1)*9)
        dm_ci_tasks = CITaskService.filter_tasks(request)
        task_list_controll = self.get_ci_task_list_controll(request,dm_ci_tasks,False)
        return task_list_controll
    
    
    def get_ci_task_list_webpart(self, request, task_type, sub_nav_action,page_title):
        dm_ci_tasks = CITaskService.get_product_ci_tasks(request, task_type, sub_nav_action)
        task_list_controll = self.get_ci_task_list_controll(request,dm_ci_tasks)
        pagefileds = {"ci_task_listcontroll":task_list_controll,"task_type":task_type,"product_id":sub_nav_action,"ci_task_page_title":page_title}
        return self.get_webpart(pagefileds, CITaskPath.task_list_webpart)
    
    def search_tasks(self,request):
        keyword=request.POST.get('keyword')
        if keyword:
            dm_ci_tasks = CITaskService.search_tasks(request)[0:9]
        else:
            dm_ci_tasks=list()
        return self.get_ci_task_list_controll(request,dm_ci_tasks,True)
    
    def filter_tasks(self,request):
        filters=request.POST.get('filters')
        if filters:
            dm_ci_tasks = CITaskService.filter_tasks(request)[0:9]
        else:
            dm_ci_tasks=list()
        return self.get_ci_task_list_controll(request,dm_ci_tasks,True)
            
    
    def get_ci_task_list_controll(self, request,dm_ci_tasks,if_full_part=True):
        ci_tasks = self.get_ci_tasks(request,dm_ci_tasks, True,if_full_part)
        pagefileds = {"ci_tasks":ci_tasks}
        return self.get_webpart(pagefileds, CITaskPath.task_list_controll)
    
    
    def get_task_config_webpart(self, request, task_id):
        dm_ci_task = CITask.objects.get(task_id)
        vm_ci_task = VM_CITask(dm_ci_task, None, True,True)
        task_plugin_menus = self.get_task_plugin_menu(request,dm_ci_task.TaskType)
        section_page_worker = CISectionPageWorker(request)
        post_section_plugins = section_page_worker.get_section_webpart(vm_ci_task.task_config.get_post_section(),task_id)
        build_section_plugins = section_page_worker.get_section_webpart(vm_ci_task.task_config.get_build_section(),task_id)
        scm_section_plugins = section_page_worker.get_section_webpart(vm_ci_task.task_config.get_scm_section(),task_id)
        pre_section_plugins = section_page_worker.get_section_webpart(vm_ci_task.task_config.get_pre_section(),task_id)
        pagefileds = {"task":vm_ci_task}
        pagefileds=dict(pagefileds, **task_plugin_menus)
        pagefileds['post_section_plugins'] = post_section_plugins
        pagefileds['build_section_plugins'] = build_section_plugins
        pagefileds['scm_section_plugins'] = scm_section_plugins
        pagefileds['pre_section_plugins'] = pre_section_plugins
        return self.get_webpart(pagefileds, CITaskPath.task_config_webpart)
    
    def get_task_plugin_menu(self,request,task_type):
        result=dict()
        result['pre_section_plugin_menu'] = self.get_task_config_plugin_menu(request,1,task_type)
        result['scm_section_plugin_menu'] = self.get_task_config_plugin_menu(request,2,task_type)
        result['build_section_plugin_menu'] = self.get_task_config_plugin_menu(request,3,task_type)
        result['post_section_plugin_menu'] = self.get_task_config_plugin_menu(request,4,task_type)
        return result
        
    
    
    def get_task_create_form(self, request):
        my_projects = ProjectCommonControllPageWorker.get_myproject_dropdown_list(self, request, 0)
        common_page_worker = CICommonControllPageWorker(request)
        deploy_services = common_page_worker.get_deploy_service_dropdown_list(0)
        ci_my_all_tasks=common_page_worker.my_ci_task_dropdown_list()
        pagefileds = {"ci_task_project":my_projects, "ci_deploy_services":deploy_services,"ci_my_all_tasks":ci_my_all_tasks}
        return self.get_webpart(pagefileds, CITaskPath.task_create_form)
    
    
    def get_task_config_plugin_menu(self, request,section_id,task_type):
        result=list()
        all_plugins = CITaskPlugin.objects.all()
        for plugin in all_plugins:
            if task_type in eval(plugin.TaskType) and section_id in eval(plugin.PluginSection):
                result.append(plugin)
        pagefileds = {"plugins":result, "plugin_role":"ci-plugin"}
        return self.get_webpart(pagefileds, CITaskPath.task_config_pop_menu)   
    
    def get_task_tag_menu(self, task,taskrole,tag_type):
        tags = list()   
        for tag in CITaskService.get_avalible_menu_tags(tag_type):
            tmp_tag = VM_Tag(tag, task.Tags)
            tags.append(tmp_tag)
        context_fileds = {'tags':tags, 'tagrole':taskrole}
        return self.get_webpart(context_fileds, ProjectTaskPath.tag_menu_template_path)
    
    def get_task_history_fullpage(self, request,task_id,task_property):
        dm_products = CITaskService.get_products_include_me(request)
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request,dm_products,0,task_id,task_property)
        ci_task_history_webpart = self.get_ci_task_history_webpart(request,task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "ci_task_history":ci_task_history_webpart}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    
    def get_task_changelog_fullpage(self, request,task_id,task_property):
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request,None,0,task_id,task_property)
        task_changelogs = self.task_changelog_webpart(request,task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "task_changelogs":task_changelogs}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    def task_changelog_webpart(self, request,task_id):
        task_changelog_list = self.task_changelog_list(task_id)
        dm_ci_task=CITask.objects.get(int(task_id))
        vm_ci_task = VM_CITask(dm_ci_task, None, True,True)
        pagefileds = {"task_changelog_list":task_changelog_list,"ci_task":vm_ci_task}
        return self.get_webpart(pagefileds, CITaskPath.task_changelog_page)
    
    
    def task_changelog_list(self,task_id):
        dm_task_histories=CITaskHistory.objects.get_task_history(int(task_id),is_active=0).order_by('-id')[0:20]
        vm_task_histories=list()
        for history in dm_task_histories:
            temp_history=VM_CITaskHistory(history,None)
            vm_task_histories.append(temp_history)
        pagefileds = {"task_histories":vm_task_histories}
        return self.get_webpart(pagefileds, CITaskPath.task_changelog_list)
    
    def task_changelog_detail(self,history_id,select_version):
        result=None
        history=CITaskHistory.objects.get(int(history_id),is_active=0)
        change_logs=CITaskHistoryService.get_change_log(history.ChangeLog)
        json_decoder=JSONDecoder()
        if change_logs:
                all_resp_changes=json_decoder.decode(change_logs['change_log'])
                for resp_changes in all_resp_changes:
                    repo=resp_changes['repo']
                    for changes in resp_changes['changes']:
                        temp_changelog=VM_CITaskChangeLog(changes,0,repo)
                        if temp_changelog.version==select_version:
                            result=temp_changelog
                            break
                    if result:
                        break;
        pagefileds = {"changefile":result}
        return self.get_webpart(pagefileds, CITaskPath.task_changelog_detail)
    
    
    def task_more_changelog_list(self,request,task_id):
        page_size=int(request.POST.get("page_size",0))
        start_index=int((page_size/9)*9)
        end_index=int(((page_size/9)+1)*9)
        dm_task_histories=CITaskHistoryService.get_finished_history(task_id)[start_index:end_index]
        vm_task_histories=list()
        for history in dm_task_histories:
            temp_history=VM_CITaskHistory(history,None)
            vm_task_histories.append(temp_history)
        pagefileds = {"task_histories":vm_task_histories}
        return self.get_webpart(pagefileds, CITaskPath.task_changelog_list)
    
    def get_ci_task_history_webpart(self, request,task_id):
        task_history_list_controll = self.get_ci_task_history_list(task_id)
        dm_ci_task=CITask.objects.get(int(task_id))
        vm_ci_task = VM_CITask(dm_ci_task, None, True,True)
        pagefileds = {"ci_task_history_list":task_history_list_controll,"ci_task":vm_ci_task}
        return self.get_webpart(pagefileds, CITaskPath.task_history_page)
    
    def get_ci_task_history_list(self,task_id):
        dm_task_histories=dm_task_histories=CITaskHistoryService.get_finished_history(task_id)[0:9]
        vm_task_histories=list()
        for history in dm_task_histories:
            tag_menu = self.get_task_tag_menu(history, "ci-history-tag-inline",2)
            temp_history=VM_CITaskHistory(history,tag_menu)
            vm_task_histories.append(temp_history)
        pagefileds = {"ci_task_histories":vm_task_histories}
        return self.get_webpart(pagefileds, CITaskPath.task_history_list)
    
    def task_more_history_list(self,request,task_id):
        page_size=int(request.POST.get("page_size",0))
        start_index=int((page_size/9)*9)
        end_index=int(((page_size/9)+1)*9)
        vm_task_histories=list()
        dm_task_histories=CITaskHistoryService.get_finished_history(task_id)[start_index:end_index]
        for history in dm_task_histories:
            tag_menu = self.get_task_tag_menu(history, "ci-history-tag-inline",2)
            temp_history=VM_CITaskHistory(history,tag_menu)
            vm_task_histories.append(temp_history)
        pagefileds = {"ci_task_histories":vm_task_histories}
        return self.get_webpart(pagefileds, CITaskPath.task_history_list)
    
    def get_downlaod_package_list(self,history_id):
        dm_task_history=CITaskHistory.objects.get(int(history_id))
        vm_history=VM_CITaskHistory(dm_task_history,None)
        pagefileds = {"build_history":vm_history}
        return self.get_webpart(pagefileds, CITaskPath.task_download_package)
    
    
    
    def build_with_parameter_fullpage(self, request,task_id,task_property):
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request,None,0,task_id,task_property)
        build_parameter_webpart =self.build_with_parameter_webpart(request, task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "build_parameter_webpart":build_parameter_webpart}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    def build_with_parameter_webpart(self, request,task_id):
        common_page_worker = CICommonControllPageWorker(request)
        ci_task=CITask.objects.get(int(task_id))
        task_parameter_groups =common_page_worker.task_parameter_dropdown_list(task_id)
        page_fileds = {"task_parameter_groups":task_parameter_groups,"ci_task":ci_task}
        return self.get_webpart(page_fileds,CITaskPath.task_build_confirm_page)
    
    
    def history_clean_fullpage(self, request,task_id,task_property):
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request,None,0,task_id,task_property)
        history_claen_page =self.history_clean_webpart(request, task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "history_claen_page":history_claen_page}
        return self.get_page(page_fileds,CITaskPath.task_index_path,request)
    
    def history_clean_webpart(self, request,task_id):
        common_page_worker = CICommonControllPageWorker(request)
        ci_task=CITask.objects.get(int(task_id))
        task_parameter_groups =common_page_worker.task_parameter_dropdown_list(task_id)
        page_fileds = {"task_parameter_groups":task_parameter_groups,"ci_task":ci_task}
        return self.get_webpart(page_fileds,CITaskPath.history_clean_page)
        
        
    def get_task_parameter_fullpage(self, request,task_id,task_property):
        left_nav_bar = self.get_task_left_bar(request)
        sub_nav_bar = self.get_task_sub_navbar(request,None,0,task_id,task_property)
        task_parameter_groups = self.get_ci_task_parameter_webpart(request,task_id)
        page_fileds = {"left_nav_bar":left_nav_bar, "sub_nav_bar":sub_nav_bar, "task_parameter_groups":task_parameter_groups}
        return self.get_page(page_fileds,CITaskPath.task_index_path, request)
    
    def get_ci_task_parameter_webpart(self, request,task_id):
        task_parameter_list_controll = self.get_ci_task_parameter_list(task_id)
        dm_ci_task=CITask.objects.get(int(task_id))
        vm_ci_task = VM_CITask(dm_ci_task, None, True,True)
        task_parameter_group_type_menu=self.task_parameter_group_type_menu(task_id)
        pagefileds = {"task_parameter_group_list":task_parameter_list_controll,"ci_task":vm_ci_task}
        pagefileds["task_parameter_group_type_menu"]=task_parameter_group_type_menu
        return self.get_webpart(pagefileds, CITaskPath.task_parameter_page)
    
    def task_parameter_group_type_menu(self,task_id):
        ci_task=CITask.objects.get(int(task_id))
        pagefileds = {"task":ci_task}
        return self.get_webpart(pagefileds, CITaskPath.task_parameter_group_type_menu)
        
    
    def get_ci_task_parameter_list(self,task_id):
        ci_task=CITask.objects.get(int(task_id))
        task_parameter_groups=CITaskParameterService.task_parameter_list(int(task_id))
        vm_groups=list()
        for group in task_parameter_groups:
            temp=VM_TaskParameterGroup(group)
            vm_groups.append(temp)
        pagefileds = {"ci_task_parameter_groups":vm_groups,"task":ci_task}
        return self.get_webpart(pagefileds, CITaskPath.task_parameter_list)
    
    def get_ci_task_parameter_edit(self,parameter_group_id):
        task_parameter_group=CITaskParameterService.task_parameter(parameter_group_id)
        vm_task_parameter_group=VM_TaskParameterGroup(task_parameter_group)
        task_plugin_list=self.parameter_group_plugin_webpart(task_parameter_group.task_id,task_parameter_group)
        pagefileds = {"task_parameter_group":vm_task_parameter_group,"task_plugin_list":task_plugin_list}
        return self.get_webpart(pagefileds, CITaskPath.task_parameter_edit)
    
    def get_task_parameter_menu(self,task_id):
        task_parameter_group=CITaskParameterService.task_parameter_list(int(task_id))
        pagefileds = {"parameter_groups":task_parameter_group}
        return self.get_webpart(pagefileds, CITaskPath.task_parameter_menu)
    
    def parameter_group_plugin_webpart(self,task_id,task_parameter_group):
        dm_ci_task=CITask.objects.get(int(task_id))
        vm_ci_task_config = VM_CITaskConfig(dm_ci_task.TaskConfig)
        result=self.parameter_group_plugin_list(vm_ci_task_config.get_pre_section()['plugins'],1,task_parameter_group)
        result=result+self.parameter_group_plugin_list(vm_ci_task_config.get_scm_section()['plugins'],2,task_parameter_group)
        result=result+self.parameter_group_plugin_list(vm_ci_task_config.get_build_section()['plugins'],3,task_parameter_group)
        result=result+self.parameter_group_plugin_list(vm_ci_task_config.get_post_section()['plugins'],4,task_parameter_group)
        return result
    
    def parameter_group_plugin_list(self,plugins,section,task_parameter_group):
        plugin_list=list()
        o=dict()
        for plugin in plugins:
            if not 'plugin_id' in plugin.keys():
                break
            plugin_id=plugin.get('plugin_id','')
            dm_plugin=CITaskPlugin.objects.get(int(plugin_id))
            dm_plugin.section_id=section
            dm_plugin.order=plugin.get('order',0)
            dm_plugin.plugin_using_name=self.get_parameter_value(plugin,'plugin_using_name','')
            dm_plugin.temp_id=str(section)+"_"+str(plugin_id)+"_"+str(dm_plugin.order)
            dm_plugin.is_enable_key=dm_plugin.temp_id+":"+plugin.get('is_enable','Off')
            dm_plugin.is_enable=plugin.get('is_enable','Off')
            if task_parameter_group.enable_plugin_settings:
                for plugin_enable in task_parameter_group.step_plugin_is_enable:
                    if plugin_enable.startswith(dm_plugin.temp_id):
                        dm_plugin.is_enable=plugin_enable.replace(dm_plugin.temp_id+",","").replace(dm_plugin.temp_id+":","")
                        dm_plugin.is_enable_key=plugin_enable
                        break
            plugin_list.append(dm_plugin)
        pagefileds={"plugin_list":plugin_list}
        return self.get_webpart(pagefileds, CITaskPath.task_parameter_plugin)
    
    def get_parameter_value(self,plugin,parameter_name,defalut=""):
        result=defalut
        if plugin!=None:
            for parameter in plugin['parameter']:
                if parameter.get('name')==parameter_name:
                    result=parameter.get('value')
        return result  
    
    def task_parameter_confirm_dialog(self,request):
        parameter_group_id=request.GET.get('group_id')
        task_parameter_group=CITaskParameterService.task_parameter(parameter_group_id)
        pre_task_parameter_group=CITaskParameterService.init_parameter_group(request)
        task_parameter_diff=VM_TaskParameterGroupDiff(task_parameter_group,pre_task_parameter_group)
        pagefileds = {"task_parameter_group":task_parameter_group,"task_parameter_diff":task_parameter_diff}
        return self.get_webpart(pagefileds, CITaskPath.task_parameter_confirm)
    
    def get_ci_tasks(self, request, all_tasks, show_tag,is_full_part):
        task_list = list()
        for dm_task in all_tasks:
            tag_menu = self.get_task_tag_menu(dm_task, "ci-task-tag-inline",1)
            parameter_group_menu=self.get_task_parameter_menu(dm_task.id)
            tmp_task = VM_CITask(dm_task, tag_menu, show_tag,is_full_part,parameter_group_menu)
            task_list.append(tmp_task)
        return task_list
    
    def get_task_sub_navbar(self, request, dm_products,sub_nav_action,task_id=0,task_property=None):
        if sub_nav_action:
            result=self.get_sub_nav_bar(request, self.subpage_model, CITaskPath.sub_nav_template_path, sub_nav_action=sub_nav_action, products=dm_products)
        else:
            dm_ci_task = CITask.objects.get(task_id)
            vm_ci_task = VM_CITask(dm_ci_task, None, False,True)
            result=self.get_property_nav_bar(request, self.task_property_model,CITaskPath.task_property_nav,property_nav_action=task_property,ci_task=vm_ci_task)
        return result
    
    def get_task_left_bar(self, request):
        return self.get_left_nav_bar(request, self.pagemodel, CITaskPath.left_nav_template_path)
        
        
        
        
    
    
    
        
        
        
        
    

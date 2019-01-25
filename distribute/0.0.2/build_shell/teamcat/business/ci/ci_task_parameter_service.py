#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from business.business_service import BusinessService
from gatesidelib.common.simplelogger import SimpleLogger
from business.common.system_config_service import SystemConfigService
from doraemon.ci.mongo_models import CITaskParameterGroup,CITaskParameter
from doraemon.project.models import Project
from doraemon.ci.models import CITask
from business.auth_user.user_service import UserService
from bson import ObjectId
import time
from doraemon.settings import EMAIL_TEMPLATES
from lib2to3.pgen2.tokenize import group
import threading
from doraemon.ci.viewmodels.vm_task_parameter_group_diff import VM_TaskParameterGroupDiff


class CITaskParameterService(BusinessService):
    '''
    classdocs
    '''
    
    @staticmethod
    def task_parameter_list(task_id):
        return CITaskParameterGroup.objects.filter(task_id=task_id).filter(is_active=True).order_by('-id')
    
    @staticmethod
    def task_parameter(id):
        result=None
        try:
            result=CITaskParameterGroup.objects.get(id=ObjectId(id))
        except Exception as ex:
            SimpleLogger.exception(ex)
        
        return result
    
    @staticmethod
    def default_parameter_group(task_id):
        result=""
        try:
            result=CITaskParameterService.task_parameter_list(task_id).filter(is_default=True)[0].id
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    @staticmethod
    def create_task_parameter(request,task_id):
        parameter_group=CITaskParameterGroup()
        default_name="parameter_group"+str(time.time())
        parameter_group.group_name=request.POST.get("group_name",default_name)
        parameter_group.task_id=int(task_id)
        parameter_group.group_type=request.POST.get("group_type",2)
#         parameter_group=CITaskParameterService.set_parameter_group_default(parameter_group,True)
        parameter_group.save()
        return parameter_group.id
    
    @staticmethod
    def delete_task_parameter(request):
        parameter_group_id=request.POST.get("group_id")
        parameter_group=CITaskParameterService.task_parameter(parameter_group_id)
        parameter_group.is_active=False
        parameter_group.save()
        return parameter_group.id
    
    @staticmethod
    def copy_task_parameter(request):
        parameter_group_id=request.POST.get("group_id")
        parameter_group=CITaskParameterService.task_parameter(parameter_group_id)
        parameter_group.id=None
        parameter_group.is_default=False
        parameter_group.save()
        return parameter_group.id
    
    @staticmethod
    def copy_parameter_group_form_task(source_taskid,target_taskid):
        task_parameter_groups=CITaskParameterService.task_parameter_list(int(source_taskid))
        for parameter_group in task_parameter_groups:
            temp_group=parameter_group
            temp_group.id=None
            temp_group.is_default=False
            temp_group.task_id=target_taskid
            temp_group.save()
    
    @staticmethod
    def has_parameters(task_id):
        result=False
        task_parameter_groups=CITaskParameterService.task_parameter_list(int(task_id))
        if len(task_parameter_groups)>0:
            result=True
        return result
    
    
    @staticmethod
    def save_task_parameter(request):
        parameter_group=CITaskParameterService.init_parameter_group(request)
#         if parameter_group.group_type=="1":
#             email_message=CITaskParameterService.prepare_email_content(request, parameter_group)
#             worker=threading.Thread(target=CITaskParameterService.send_notification_email,args=(parameter_group.task_id,email_message))
#             worker.start()
        parameter_group.save()
        return parameter_group.id
    
    @staticmethod
    def send_notification_email(task_id,email_message):
        ci_task=CITask.objects.get(int(task_id))
        email_list = CITaskParameterService.get_email_list(ci_task.Project)
        email_config = SystemConfigService.get_email_config()
        subject="发布参数值正在被修改！！！"
        CITaskParameterService.send_email(email_config, email_list, email_message, subject)
    
    @staticmethod
    def prepare_email_content(request,parameter_group):
        ci_task=CITask.objects.get(int(parameter_group.task_id))
        email_template=EMAIL_TEMPLATES['ParameterGroupChangedPage']
        summary_info= "Task ["+ci_task.TaskName+"]  Release参数组：[" + parameter_group.group_name + "]参数值变更"
        email_message = CITaskParameterService.create_email_message(request,parameter_group,ci_task.Project,summary_info,email_template)
        return email_message 

    
    @staticmethod
    def create_email_message(request,parameter_group,project_id,summary_info,email_template_path):
        email_templates = open(email_template_path, 'rb').read().decode()
        project= Project.objects.get(project_id)
        projectname = project.PBTitle
        changer = UserService.get_user(request.user.id)
        email_templates = email_templates.replace("$Subject",summary_info)
        email_templates = email_templates.replace("$ProjectName",projectname)
        email_templates = email_templates.replace("$GroupName",parameter_group.group_name)
        email_templates = email_templates.replace("$Changer", str(changer.last_name + changer.first_name))
        email_templates = CITaskParameterService.parameter_change_detail(request, email_templates)
        return email_templates
    @staticmethod
    def parameter_change_detail(request,email_templates):
        email_template=EMAIL_TEMPLATES['ParameterGroupChangedDetail']
        pre_task_parameter_group=CITaskParameterService.init_parameter_group(request)
        task_parameter_group=CITaskParameterService.task_parameter(pre_task_parameter_group.id)
        task_parameter_diff=VM_TaskParameterGroupDiff(task_parameter_group,pre_task_parameter_group)
        email_templates = email_templates.replace("$GroupPropertyChange",CITaskParameterService.parameter_change_detail_content(task_parameter_diff.parameter_group_property_diff(),email_template))
        email_templates = email_templates.replace("$ParameterChange",CITaskParameterService.parameter_change_detail_content(task_parameter_diff.parameter_diff(),email_template))
        email_templates = email_templates.replace("$ParameterNew",CITaskParameterService.parameter_change_detail_content(task_parameter_diff.parameter_new(),email_template))
        email_templates = email_templates.replace("$ParameterDelete",CITaskParameterService.parameter_change_detail_content(task_parameter_diff.parameter_delete(),email_template))
        return email_templates
        
    @staticmethod
    def parameter_change_detail_content(change_detail,detail_email_templates):
        detail_email_templates = open(detail_email_templates,'rb').read().decode()
        result=""
        for diff in change_detail:
            email_templates=detail_email_templates.replace("$FieldName",str(diff.field_name))
            email_templates=email_templates.replace("$FieldOldValue",str(diff.field_old_value))
            email_templates=email_templates.replace("$FieldNewValue",str(diff.field_new_value))
            result=result+email_templates
        return result
    
    
   
    @staticmethod
    def init_parameter_group(request):
        if request.method=="GET":
            source=request.GET
        else:
            source=request.POST
        parameter_group_id=source.get("group_id")
        
        key_list=source.getlist("key")
        value_list=source.getlist("value")
        description_list=source.getlist("description")
        parameter_list=list()
        parameter_group=CITaskParameterService.task_parameter(parameter_group_id)
        for (key,value,desc) in zip(key_list,value_list,description_list):
            temp=CITaskParameter()
            temp.key=key
            temp.value=value
            temp.description=desc
            parameter_list.append(temp)
        parameter_group.parameters=None
        parameter_group.parameters=parameter_list
        parameter_group.group_name=source.get("group_name")
        parameter_group.description=source.get("group_description")
        parameter_group.group_type=source.get("group_type")
        print(bool("0"))
        if source.get("enable_plugin_settings","False")=="True":
            parameter_group.enable_plugin_settings=True
        else:
            parameter_group.enable_plugin_settings=False
        if parameter_group.enable_plugin_settings:
            parameter_group.step_plugin_is_enable=source.getlist("plugin_is_enable")
        else:
            parameter_group.step_plugin_is_enable=list()
        is_default=bool(source.get("group_is_default",False))
        parameter_group=CITaskParameterService.set_parameter_group_default(parameter_group,is_default)
        print("#########################################")
        print(parameter_group.enable_plugin_settings)
        return parameter_group
    
    
    @staticmethod
    def set_parameter_group_default(parameter_group,is_default):
        if is_default:
            parameter_groups=CITaskParameterService.task_parameter_list(parameter_group.task_id)
            for group in parameter_groups:
                group.is_default=False
                if not group.group_type:
                    group.group_type=2
                group.save()
            parameter_group.is_default=is_default
        return parameter_group

          
        
        
        
        
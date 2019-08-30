#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from business.business_service import BusinessService
from gatesidelib.common.simplelogger import SimpleLogger
from business.common.system_config_service import SystemConfigService
from teamvision.ci.mongo_models import CITaskParameterGroup,CITaskStage
from teamvision.ci import mongo_models

from bson import ObjectId



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
    def save_step_settings(parameter_group_id):
        parameter_group = CITaskParameterService.task_parameter(parameter_group_id)
        if parameter_group.step_settings is None or len(parameter_group.step_settings) == 0:
            result = list()
            step_ids = list()
        else:
            result = parameter_group.step_settings
            step_ids = [str(step_setting.step_id) for step_setting in parameter_group.step_settings]
        task_stages = CITaskStage.objects.all().filter(task_id=parameter_group.task_id).order_by('stage_order_index')
        task_step_ids = list()
        stage_ids = list()
        for stage in task_stages:
            stage_ids.append(str(stage.id))
            steps = mongo_models.CITaskStep.objects.all().filter(stage_id=str(stage.id)).order_by(
                    'step_order_index')
            for step in steps:
                task_step_ids.append(str(step.id))
                if str(step.id) not in step_ids:
                    result.append(CITaskParameterService.init_step_setting(step,stage))
                if parameter_group is not None and parameter_group.step_settings is not None:
                    for step_setting in parameter_group.step_settings:
                        if step_setting.step_id == str(step.id):
                            step_setting.desc = step.purpose_name
                            step_setting.stage_title = stage.stage_title

        final_result = list()
        for step_setting in result:
            if str(step_setting.step_id) in task_step_ids and str(step_setting.stage_id) in stage_ids:
                if step_setting not in final_result:
                    final_result.append(step_setting)

        parameter_group.step_settings = final_result
        parameter_group.save()

    @staticmethod
    def init_step_setting(step,stage):
        temp_step_settings = mongo_models.ParameterStepSettings()
        temp_step_settings.stage_id = str(stage.id)
        if stage.is_on:
            temp_step_settings.is_on = step.is_on
        else:
            temp_step_settings.is_on = stage.is_on
        temp_step_settings.step_id = str(step.id)
        temp_step_settings.step_order_index = step.step_order_index
        temp_step_settings.desc = step.purpose_name
        temp_step_settings.stage_title = stage.stage_title
        temp_step_settings.step_name = step.step_config['step_name']
        return temp_step_settings


    
    @staticmethod
    def copy_task_parameter(parameter_group_id):
        parameter_group=CITaskParameterService.task_parameter(parameter_group_id)
        parameter_group.id=None
        parameter_group.group_name = parameter_group.group_name+'_Copy'
        parameter_group.is_default=False
        parameter_group.save()
        return parameter_group
    
    @staticmethod
    def copy_parameter_group_form_task(source_taskid,target_taskid):
        task_parameter_groups=CITaskParameterService.task_parameter_list(int(source_taskid))
        for parameter_group in task_parameter_groups:
            temp_group=parameter_group
            temp_group.id=None
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
    def set_parameter_group_default(parameter_group,is_default):
        if is_default:
            parameter_groups=CITaskParameterService.task_parameter_list(parameter_group.task_id)
            for group in parameter_groups:
                group.is_default=False
                if str(group.id) == str(parameter_group.id):
                    group.is_default = True
                if not group.group_type:
                    group.group_type = 2
                group.save()

          
        
        
        
        
#coding=utf-8
'''
Created on 2016-7-6

@author: zhangtiande
'''
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.ci.mongo_models import CITaskParameterGroup,CITaskStage,CITaskDefaultStage
from teamvision.ci import mongo_models
from bson import ObjectId

class CITaskConfigService(object):
    '''
    classdocs
    '''

    @staticmethod
    def task_stage_list(task_id):
        stage_list = CITaskStage.objects.filter(task_id=task_id).filter(is_active=True).order_by('stage_order_index')
        return stage_list

    @staticmethod
    def task_stage_steps(stage_id):
        return mongo_models.CITaskStep.objects.all().filter()(stage_id=str(stage_id)).order_by('step_order_index')


    @staticmethod
    def init_stage_list(stage_list):
        result = list()
        if len(stage_list) == 0:
            temp = mongo_models.CITaskStage()
            temp.svn_steps = list()
            temp.git_steps = list()
            temp.android_build_steps = list()
            temp.command_steps = list()
            temp.gat_apitest_steps = list()
            temp.gat_uitest_steps = list()
            temp.ios_build_steps = list()
            temp.ssh_steps = list()
            temp.svn_steps.append(mongo_models.CITaskSVNStep())
            temp.git_steps.append(mongo_models.CITaskGitStep())
            temp.android_build_steps.append(mongo_models.CITaskAndroidStep())
            temp.command_steps.append(mongo_models.CITaskCommandStep())
            temp.gat_apitest_steps.append(mongo_models.CITaskGATAPITestStep())
            temp.gat_uitest_steps.append(mongo_models.CITaskGATUITestStep())
            temp.ios_build_steps.append(mongo_models.CITaskIOSStep())
            temp.ssh_steps.append(mongo_models.CITaskSSHStep())
            result.append(temp)
        return result


    @staticmethod
    def task_stage(id):
        result = None
        try:
            result = CITaskStage.objects.get(id=ObjectId(id))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    @staticmethod
    def copy_task_stage(task_id,target_task_id):
        stage_list = CITaskConfigService.task_stage_list(task_id)
        for stage in stage_list:
            s_stageid = stage.id
            temp_stage = stage
            temp_stage.task_id = target_task_id
            temp_stage.id = None
            temp_stage.save()
            CITaskConfigService.copy_stage_step(s_stageid,temp_stage.id)


    @staticmethod
    def copy_default_stage(task_id,target_task_id):
        default_stage = CITaskConfigService.task_default_sage(task_id)
        default_stage.task_id = target_task_id
        default_stage.id = None
        default_stage.save()

    @staticmethod
    def copy_stage_step(stage_id, target_stage_id):
        step_list = CITaskConfigService.task_stage_steps(str(stage_id))
        for step in step_list:
            temp_step = step
            temp_step.id = None
            temp_step.stage_id = str(target_stage_id)
            temp_step.save()

    @staticmethod
    def delete_task_stage(task_id):
        CITaskConfigService.delete_default_stage(task_id)
        stage_list = CITaskConfigService.task_stage_list(task_id)
        for stage in stage_list:
            CITaskConfigService.delete_steps(stage.id)
        stage_list.delete()

    @staticmethod
    def delete_default_stage(task_id):
        try:
            default_stage = CITaskConfigService.task_default_sage(task_id)
            default_stage.delete()
        except Exception as ex:
            SimpleLogger.exception(ex)


    @staticmethod
    def delete_steps(stage_id):
        result = None
        try:
            result = mongo_models.CITaskStep.objects.all().filter()(stage_id=stage_id)
            result.delete()
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


    @staticmethod
    def task_step(id):
        result = None
        try:
            result = mongo_models.CITaskStep.objects.get(id=ObjectId(id))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


    @staticmethod
    def task_default_sage(task_id):
        result = None
        default_stage_queryset = CITaskDefaultStage.objects.all().filter(task_id=task_id)
        if len(default_stage_queryset)>0:
            result  = default_stage_queryset[0]
        return result
    
    
    

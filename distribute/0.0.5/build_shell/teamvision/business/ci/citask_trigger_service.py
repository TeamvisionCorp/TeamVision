#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from teamvision.ci.models import CITaskApiTrigger,CITask
from business.ci.ci_task_service import CITaskService
from business.business_service import BusinessService


class CITaskTriggerService(BusinessService):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_all_triggers():
        return CITaskApiTrigger.objects.all()
    
    
    @staticmethod
    def create_start_trigger(request,trigger_data,user):
        trigger=CITaskApiTrigger()
        trigger=CITaskTriggerService.init_trigger(trigger_data,trigger)
        trigger.IsActive=1
        trigger.ActionType = 1
        start_result  = CITaskService.start_ci_task(request,trigger.TaskID,trigger.BuildParameter,0)
        trigger.TaskQueueUUID = start_result[2]
        trigger.save()
        CITaskTriggerService.log_create_activity(user, trigger)
        return trigger



    @staticmethod
    def create_stop_trigger(request,trigger_data,user):
        tr_uuid = trigger_data.get('TriggerUUID',None)
        trigger = None
        if tr_uuid:
            trigger=CITaskApiTrigger.objects.get_by_truuid(tr_uuid)
            if trigger:
                trigger=CITaskTriggerService.init_trigger(trigger_data,trigger)
                trigger.IsActive=1
                trigger.ActionType = 2
                stop_result  = CITaskService.stop_ci_task(request,trigger.TaskID,trigger.TaskQueueUUID)
                trigger.TaskQueueUUID = stop_result[2]
                trigger.save()
                CITaskTriggerService.log_create_activity(user, trigger)
        return trigger
            
    

    @staticmethod
    def init_trigger(trigger_data,trigger):
        tmp_trigger=trigger
        tmp_trigger.TriggerName=trigger_data.get('TriggerName')
        tmp_trigger.TriggerUUID=trigger_data.get('TriggerUUID')
        tmp_trigger.TaskID=trigger_data.get('TaskID')
        tmp_trigger.Branch=trigger_data.get('Branch')
        tmp_trigger.CodeAddress=trigger_data.get('CodeAddress')
        tmp_trigger.CommitID=trigger_data.get('CommitID')
        tmp_trigger.BuildParameter=trigger_data.get('BuildParameter')

        return tmp_trigger


    @staticmethod
    def log_create_activity(user,trigger):
        CITaskApiTrigger.objects.log_action(0, trigger.id, trigger.TriggerName,ADDITION,"触发任务执行",-1,CITaskTriggerService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,trigger):
        CITaskApiTrigger.objects.log_action(0, trigger.id, trigger.TriggerName,DELETION,"删除任务触发",-1,CITaskTriggerService.ActionLogType.CI)
    
    @staticmethod
    def log_change_activity(user,trigger):
        CITaskApiTrigger.objects.log_action(0,trigger.id,trigger.TriggerName,CHANGE,"修改任务触发",-1,CITaskTriggerService.ActionLogType.CI)
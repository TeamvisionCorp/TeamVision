#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from teamvision.ci.models import CITaskFlow,CITaskFlowSection,CITaskFlowHistory
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from teamvision.project.models import Project
from business.project.project_service import ProjectService
from business.project.version_service import VersionService
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_service import CITaskService
from business.business_service import BusinessService
from business.ci.ci_taskflow_section_service import CITaskFlowSectionService
from teamvision.home.models import TaskQueue
from gatesidelib.datetimehelper import DateTimeHelper
from teamvision.ci.datamodels.task_queue_command_enum import TaskQueueCommandTypeEnum
from teamvision.ci.datamodels.task_queue_status_enum import TaskQueueStatusEnum
import uuid


class CITaskFlowService(BusinessService):
    '''
    classdocs
    '''
    @staticmethod
    def get_my_taskflows(request,product_id):
        prodcut_tasks=CITaskFlowService.get_product_taskflows(request,product_id)
        return prodcut_tasks

    
    @staticmethod
    def get_product_taskflows(request,product_id):
        result = list()
        try:
            my_projects=ProjectService.get_projects_include_me(request)
            my_project_ids=[project.id for project in my_projects]
            if product_id.upper()=="ALL":
                result=CITaskFlow.objects.all().filter(Project__in=my_project_ids).order_by('-LastHistory')
            else:
                product_projects=Project.objects.all().filter(Product=int(product_id)).filter(id__in=my_project_ids)
                result=CITaskFlow.objects.all().filter(Project__in=product_projects).filter.order_by('-LastHistory')
        except Exception as ex:
            SimpleLogger.error(ex)
        return result

    @staticmethod
    def create_taskflow(validate_data,user):
        citasks = validate_data.get('CITasks','0,')
        print(validate_data)
        ci_taskflow=CITaskFlow()
        ci_taskflow=CITaskFlowService.init_taskflow(validate_data, ci_taskflow)
        ci_taskflow.IsActive=1
        ci_taskflow.Creator=user.id
        ci_taskflow.save()
        CITaskFlowSectionService.create_section("默认",ci_taskflow.id,1,citasks)
        CITaskFlowService.log_create_activity(user, ci_taskflow)
        return ci_taskflow
    


    @staticmethod
    def copy_taskflow(user,flow_id):
        taskflow = CITaskFlow.objects.get(int(flow_id))
        taskflow.FlowName= taskflow.FlowName+"_Copy"
        taskflow.id=None
        taskflow.Creator=user.id
        taskflow.save()
        CITaskFlowSectionService.copy_section(flow_id,taskflow.id)
        CITaskFlowService.log_create_activity(user, taskflow)
    
    
    @staticmethod
    def delete_taskflow(user,flow_id):
        taskflow = CITaskFlow.objects.get(int(flow_id))
        taskflow.IsActive = 0
        taskflow.save()
        CITaskFlowService.log_delete_activity(user, taskflow)

    @staticmethod
    def start_taskflow(request,flow_id):
        taskflow = CITaskFlow.objects.get(int(flow_id))
        queuetask=TaskQueue()
        queuetask.EnqueueTime=DateTimeHelper.get_local_now()
        queuetask.TaskType=6
        queuetask.Command= TaskQueueCommandTypeEnum.TaskQueueCommandType_Start
        queuetask.Priority=2
        queuetask.Status = TaskQueueStatusEnum.QueueTaskStatus_New
        queuetask.TaskID=int(flow_id)
        queuetask.TaskUUID=uuid.uuid1()
        queuetask.FromName=request.user.id
        queuetask.save()
        # taskflow.LastHistory = CITaskFlowService.save_taskflow_history(request,taskflow,queuetask.TaskUUID)
        taskflow.LastRunTime = DateTimeHelper.get_local_now()
        taskflow.save(update_fields=['LastRunTime'])
        message="任务流 ["+taskflow.FlowName+"] 的执行指令已经下发，请耐心等待。"
        return message
    
    @staticmethod
    def save_taskflow_history(request,task_flow,tq_uuid):
        flow_history=CITaskFlowHistory()
        flow_history.TaskFlow=task_flow.id
        flow_history.Status=0
        flow_history.TQUUID = tq_uuid
        if request.user.id!=None:
            flow_history.StartedBy=request.user.id
        else:
            flow_history.StartedBy=0
        flow_history.save()
        return flow_history.id
    
    @staticmethod
    def get_project_latest_version(project_id):
        result=0
        version=VersionService.get_latest_version(project_id)
        if version:
            result=version.id
        return result
    

    
    @staticmethod
    def stop_task_flow(request,task_id):
        command_type=TaskQueueCommandTypeEnum.TaskQueueCommandType_Stop
        tq_uuid=request.GET.get("TaskUUID","")
        tq_tasks = TaskQueue.objects.all().filter(TaskUUID=tq_uuid).filter(Command=command_type)
        if not tq_tasks.exists():
            task_flow=CITaskFlow.objects.get(int(task_id))
            queuetask=TaskQueue()
            queuetask.EnqueueTime=DateTimeHelper.get_local_now(8)
            queuetask.TaskType=task_flow.TaskType
            queuetask.Command=command_type
            queuetask.Priority=7
            queuetask.Status =TaskQueueStatusEnum.QueueTaskStatus_New
            queuetask.TaskID=int(task_id)
            queuetask.TaskUUID=tq_uuid
            queuetask.save()
        else:
            queuetask = tq_tasks[0]

        message="任务ID为:"+str(task_id)+"的取消执行指令已经下发，请耐心等待。"
        CITaskFlowService.send_task_enqueue_message()
        return [queuetask.id,message,queuetask.TaskUUID]


    

    @staticmethod
    def init_taskflow(formdata,task_flow):
        tmp_task_flow=task_flow
        tmp_task_flow.FlowName=formdata.get('FlowName')
        tmp_task_flow.Project=int(formdata.get('Project'))
        tmp_task_flow.Description=formdata.get('Description')
        return tmp_task_flow
    
    
    

    

           
    

    @staticmethod
    def log_create_activity(user,task_flow):
        CITaskFlow.objects.log_action(user.id,task_flow.id,task_flow.FlowName,ADDITION,"创建了CI任务",task_flow.Project,CITaskFlowService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,task_flow):
        CITaskFlow.objects.log_action(user.id,task_flow.id,task_flow.FlowName,DELETION,"删除了CI任务",task_flow.Project,CITaskFlowService.ActionLogType.CI)

    @staticmethod
    def log_change_activity(user,task_flow):
        CITaskFlow.objects.log_action(user.id,task_flow.id,task_flow.FlowName,CHANGE,"修改了CI任务",task_flow.Project,CITaskFlowService.ActionLogType.CI)
    
    @staticmethod
    def log_build_activity(user_id,task_flow):
        CITaskFlow.objects.log_action(user_id,task_flow.id,task_flow.FlowName,CHANGE,"构建了CI任务",task_flow.Project,CITaskFlowService.ActionLogType.CI)
        
        
        
        
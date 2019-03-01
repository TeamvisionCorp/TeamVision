# coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from teamvision.ci.models import CITaskFlowSection, CITaskFlow, CITaskFlowHistory, CIFlowSectionHistory
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION, CHANGE, ADDITION
from business.business_service import BusinessService
from teamvision.home.models import TaskQueue
from gatesidelib.datetimehelper import DateTimeHelper
from teamvision.ci.datamodels.task_queue_command_enum import TaskQueueCommandTypeEnum
from teamvision.ci.datamodels.task_queue_status_enum import TaskQueueStatusEnum
import uuid


class CITaskFlowSectionService(BusinessService):
    '''
    classdocs
    '''

    @staticmethod
    def create_section(section_name, flow_id, section_order, citasks):
        ci_taskflow_section = CITaskFlowSection()
        ci_taskflow_section.SectionName = section_name
        ci_taskflow_section.TaskFlow = int(flow_id)
        ci_taskflow_section.SectionOrder = int(section_order)
        ci_taskflow_section.CITasks = citasks
        ci_taskflow_section.IsActive = 1
        ci_taskflow_section.save()
        return ci_taskflow_section

    @staticmethod
    def copy_section(source_flow_id, target_flow_id):
        ci_taskflow_sections = CITaskFlowSection.objects.flow_sections(int(source_flow_id))
        for section in ci_taskflow_sections:
            section.TaskFlow = target_flow_id
            section.id = None
            section.save()

    @staticmethod
    def start_flowsection(request, section_id):
        flow_section = CITaskFlowSection.objects.get(int(section_id))
        message = "任务阶段 [" + flow_section.SectionName + "] 的执行指令已经下发，请耐心等待。"
        queuetask = TaskQueue()
        queuetask.EnqueueTime = DateTimeHelper.get_local_now()
        queuetask.TaskType = 7
        queuetask.Command = TaskQueueCommandTypeEnum.TaskQueueCommandType_Start
        queuetask.Priority = 2
        queuetask.Status = TaskQueueStatusEnum.QueueTaskStatus_New
        queuetask.TaskID = int(section_id)
        queuetask.TaskUUID = uuid.uuid1()
        queuetask.FromName=request.user.id
        queuetask.save()
        task_flow = CITaskFlow.objects.get(flow_section.TaskFlow)
        # flow_history = CITaskFlowSectionService.save_taskflow_history(request, task_flow,queuetask.TaskUUID)
        # CITaskFlowSectionService.save_section_history(request, flow_section, flow_history)
        # task_flow.LastHistory = flow_history.id
        task_flow.LastRunTime = DateTimeHelper.get_local_now()
        task_flow.save(update_fields=['LastRunTime'])
        return message

    @staticmethod
    def save_taskflow_history(request, task_flow,tq_uuid):
        flow_history = CITaskFlowHistory()
        flow_history.TaskFlow = task_flow.id
        flow_history.TQUUID = tq_uuid
        flow_history.Status = 0
        if request.user.id != None:
            flow_history.StartedBy = request.user.id
        else:
            flow_history.StartedBy = 0
        flow_history.save()
        return flow_history

    @staticmethod
    def save_section_history(request, section, flow_history):
        section_history = CIFlowSectionHistory()
        section_history.TaskFlow = flow_history.TaskFlow
        section_history.TaskFlowHistory = flow_history.id
        section_history.TQUUID = flow_history.TQUUID
        section_history.Status = 0
        if request.user.id != None:
            section_history.StartedBy = request.user.id
        else:
            section_history.StartedBy = 0
        section_history.save()
        return section_history.id

#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from doraemon.ci.models import CITask,CITaskHistory
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from doraemon.project.models import Product,Project,Tag
from business.project.project_service import ProjectService
from business.project.version_service import VersionService
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_config_service import CITaskConfigService
from business.ci.ci_task_history_service import CITaskHistoryService
from business.business_service import BusinessService
from business.common.redis_service import RedisService
from business.common.mongodb_service import MongoDBService
from doraemon.api.ci.mongo_models import PackgeMongoFile
from doraemon.home.models import TaskQueue
from gatesidelib.datetimehelper import DateTimeHelper
from business.common.system_config_service import SystemConfigService
from doraemon.ci.datamodels.task_queue_command_enum import TaskQueueCommandTypeEnum
from doraemon.ci.datamodels.task_queue_status_enum import TaskQueueStatusEnum
import uuid
from business.common.file_info_service import FileInfoService


class CITaskService(BusinessService):
    '''
    classdocs
    '''
    
    
    
    @staticmethod
    def get_products_include_me(request):
        my_projects=ProjectService.get_projects_include_me(request)
        prodcut_ids=list()
        for project in my_projects:
            if project.Product not in prodcut_ids:
                prodcut_ids.append(project.Product)
        return Product.objects.all().filter(id__in=prodcut_ids)
    
    
    @staticmethod
    def get_ci_tasks_recently_build(request,task_type,product_id):
        result = list()
        try:
            result=CITaskService.get_product_ci_tasks(request, task_type, product_id).filter(LastHistory__exclude=(0,))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    @staticmethod
    def get_my_ci_tasks(request,task_type,product_id):
        prodcut_tasks=CITaskService.get_product_ci_tasks(request,task_type,product_id)
        return prodcut_tasks
    @staticmethod
    def get_latest_history(task_id):
        result=None
        historys=CITaskHistory.objects.all().filter(CITaskID=task_id).order_by('-id')
        if historys:
            result=historys[0]
        return result
    
    @staticmethod
    def get_product_ci_tasks(request,task_type,product_id):
        result = list()
        try:
            my_projects=ProjectService.get_projects_include_me(request)
            my_project_ids=[project.id for project in my_projects]
            if product_id.upper()=="ALL":
                if task_type!=0:
                    result=CITask.objects.all().filter(TaskType=task_type).filter(Project__in=my_project_ids).order_by('-LastHistory')
                else:
                    result=CITask.objects.all().filter(Project__in=my_project_ids).order_by('-LastHistory')
            else:
                product_projects=Project.objects.all().filter(Product=int(product_id)).filter(id__in=my_project_ids)
                result=CITask.objects.all().filter(Project__in=product_projects).filter(TaskType=task_type).order_by('-LastHistory')
        except Exception as ex:
            SimpleLogger.error(ex)
        return result
    
    @staticmethod
    def search_tasks(request):
        result=list()
        keyword=request.POST.get('keyword','all')  #get search keyword
        task_type=int(request.POST.get('task_type',0)) #get task type
        product_id=request.POST.get('product_id','all') # get product type
            
        # all my tasks include the built task recently and the tasks belong to product
        built_tasks=CITaskService.get_ci_tasks_recently_build(request,task_type,product_id)
        product_tasks=CITaskService.get_product_ci_tasks(request,task_type,product_id)
        
        # if keyword is all,then return all my tasks
        # else filter with keyword and return the rest tasks
        if keyword.upper() =='ALL':
            result.extend(built_tasks)
            for task in product_tasks:
                if task not in result:
                    result.append(task)
        else:
            built_tasks=[task for task in built_tasks if keyword.upper() in task.TaskName.upper()]
            product_task=product_tasks.filter(TaskName__icontains=keyword)
            result.extend(built_tasks)
            for task in product_task:
                if task not in result:
                    result.append(task)
        return result
                
    @staticmethod
    def filter_tasks(request):
        result=CITaskService.search_tasks(request)
        project_ids=request.POST.get('project_id')
        tag_ids=request.POST.get('tag_id')
        if project_ids!="":
            result=[task for task in result if task.Project in eval(project_ids)]
        match_tag_task=list()
        if tag_ids!="":
            for task in result:
                for tag in eval(tag_ids):
                    if task.Tags and tag in eval(task.Tags):
                        match_tag_task.append(task)
                        break;
            result=match_tag_task                
        return result
            
        
        
                
    
    
    @staticmethod
    def create_ci_task(validate_data,user):
        task_type=int(validate_data.get('TaskType'))
        ci_task=CITask()
        if task_type:
            ci_task=CITask()
            ci_task=CITaskService.init_ci_task(validate_data, ci_task)
            ci_task.IsActive=1
            ci_task.Creator=user.id
            ci_task.TaskConfig=CITaskConfigService.create_config()
            ci_task.save()
        else:
            ci_task=CITaskService.copy_ci_task(validate_data,user)
        CITaskService.log_create_activity(user, ci_task)
        return ci_task
            
    
    
    @staticmethod
    def save_task_config(request,ci_taskid):
        ci_task=CITask.objects.get(int(ci_taskid))
        CITaskConfigService.save_task_config(request, ci_task)
        CITaskService.log_change_activity(request.user, ci_task)
    
    
    
    @staticmethod
    def copy_ci_task(validate_data,user):
        task_id=int(validate_data.get('CopyTaskID'))
        ci_task=CITask.objects.get(int(task_id))
        ci_task.TaskName=validate_data.get('TaskName')
        ci_task.Project=validate_data.get('Project')
        ci_task.BuildVersion=0
        ci_task.id=None
        ci_task.Creator=user.id
        ci_task.save()
        new_config=CITaskConfigService.copy_config(ci_task.TaskConfig,ci_task.id,ci_task.TaskName)
        ci_task.TaskConfig=new_config
        ci_task.save()
        CITaskParameterService.copy_parameter_group_form_task(task_id,ci_task.id)
        CITaskService.log_create_activity(user, ci_task)
        return ci_task
    
    
    @staticmethod
    def delete_ci_task(request,task_id):
        ci_task=CITask.objects.get(int(task_id))
        CITaskConfigService.delete_config(ci_task.TaskConfig)
        CITaskHistoryService.clean_all_history(task_id,True)
        ci_task.IsActive=0
        ci_task.save()
        CITaskService.log_delete_activity(request.user, ci_task)
    
    @staticmethod
    def clean_task_history(request,task_id):
        ci_task=CITask.objects.get(int(task_id))
        CITaskHistoryService.clean_all_history(task_id,False)
        CITaskService.log_clean_activity(request.user, ci_task)
    
        
    @staticmethod
    def start_ci_task(request,task_id,parameter_group_id,project_version):
        ci_task=CITask.objects.get(int(task_id))
        queuetask=TaskQueue()
        queuetask.EnqueueTime=DateTimeHelper.get_local_now()
        queuetask.TaskType=ci_task.TaskType
        queuetask.Command=TaskQueueCommandTypeEnum.TaskQueueCommandType_Start
        queuetask.Priority=2
        queuetask.Status =TaskQueueStatusEnum.QueueTaskStatus_New
        queuetask.TaskID=int(task_id)
        queuetask.TaskUUID=uuid.uuid1()
        if parameter_group_id:
            queuetask.BuildParameterID=parameter_group_id
        else:
            queuetask.BuildParameterID=CITaskParameterService.default_parameter_group(int(task_id))
        queuetask.save()
        ci_task.BuildVersion=ci_task.BuildVersion+1
        if str(project_version) == '0':
            project_version = VersionService.get_latest_version(ci_task.Project)
            if project_version:
                project_version = project_version.id
            else:
                project_version = 0
        ci_task.LastHistory = CITaskService.save_ci_taskhistory(request,queuetask,ci_task,project_version)
        ci_task.save(update_fields=['BuildVersion','LastHistory'])
        message="任务ID为:"+str(task_id)+"的执行指令已经下发，请耐心等待。"
        user_id=0
        if request.user.id:
            user_id=request.user.id
        CITaskService.log_build_activity(user_id, ci_task)
        CITaskService.send_task_enqueue_message()
        return [queuetask.id,message,queuetask.TaskUUID]
    
    @staticmethod
    def save_ci_taskhistory(request,task_queue,ci_task,project_version):
        if not project_version:
            project_latest_version=CITaskService.get_project_latest_version(ci_task.Project)
        else:
            project_latest_version=int(project_version)
        task_history=CITaskHistory()
        task_history.CITaskID=ci_task.id
        task_history.TaskUUID = task_queue.TaskUUID
        task_history.TaskQueueID=task_queue.id
        task_history.IsActive=1
        task_history.BuildStatus=0
        if request.user.id!=None:
            task_history.StartedBy=request.user.id
        else:
            task_history.StartedBy=0
        task_history.BuildVersion=ci_task.BuildVersion
        task_history.ProjectVersion=project_latest_version
        task_history.BuildParameterID=task_queue.BuildParameterID
        task_history.save()
        return task_history.id


    @staticmethod
    def update_ci_taskhistory(tq_id,file_id,file_type):
        task_history=CITaskHistory.objects.get_by_tqid(tq_id)
        if file_type=='1':
            if task_history.PackageID:
                task_history.PackageID=task_history.PackageID+str(file_id)+','
            else:
                task_history.PackageID=str(file_id)+','
        if file_type=='2':
            if task_history.LogFileID:
                task_history.LogFileID=task_history.LogFileID+str(file_id)+','
            else:
                task_history.LogFileID=str(file_id)+','
        task_history.save()

    
    @staticmethod
    def stop_ci_task(request,task_id):
        command_type=TaskQueueCommandTypeEnum.TaskQueueCommandType_Stop
        tq_uuid=request.GET.get("TaskUUID","")
        tq_tasks = TaskQueue.objects.all().filter(TaskUUID=tq_uuid).filter(Command=command_type)
        if not tq_tasks.exists():
            ci_task=CITask.objects.get(int(task_id))
            queuetask=TaskQueue()
            queuetask.EnqueueTime=DateTimeHelper.get_local_now()
            queuetask.TaskType=ci_task.TaskType
            queuetask.Command=command_type
            queuetask.Priority=7
            queuetask.Status =TaskQueueStatusEnum.QueueTaskStatus_New
            queuetask.TaskID=int(task_id)
            queuetask.TaskUUID=tq_uuid
            queuetask.save()
        else:
            queuetask = tq_tasks[0]

        message="任务ID为:"+str(task_id)+"的取消执行指令已经下发，请耐心等待。"
        CITaskService.send_task_enqueue_message()
        return [queuetask.id,message,queuetask.TaskUUID]


    @staticmethod
    def send_task_enqueue_message():
        RedisService.websocket_publish_message("TASKSTATUSCHANGE",'Task enqueue now!')
    

    @staticmethod
    def init_ci_task(formdata,ci_task):
        tmp_ci_task=ci_task
        tmp_ci_task.TaskName=formdata.get('TaskName')
        tmp_ci_task.Project=formdata.get('Project')
        tmp_ci_task.TaskType=formdata.get('TaskType')
        historyCleanStrategy=formdata.get('HistoryCleanStrategy',5)
        if historyCleanStrategy=="":
            historyCleanStrategy=5
        tmp_ci_task.HistoryCleanStrategy=historyCleanStrategy
        tmp_ci_task.Schedule=formdata.get('time_trigger',"")
        if int(tmp_ci_task.TaskType)==3:
            tmp_ci_task.DeployService=formdata.get('DeployService',0)
        tmp_ci_task.Description=formdata.get('Description',"")
        return tmp_ci_task
    
    
    
    @staticmethod
    def upload_package(request):
        result=0
        tq_id=request.POST.get('tq_id','')
        file_type=request.POST.get('file_type','')
        upload_file=request.FILES['upload_file']
        max_file_size=SystemConfigService.get_upload_file_maxsize()
        file_wihte_list=SystemConfigService.get_file_type_white_list()
        if CITaskService.validate_upload_file(upload_file,max_file_size,file_wihte_list):
            mongo_fileid=MongoDBService.save_file(upload_file,PackgeMongoFile)
            result=FileInfoService.add_file(0,mongo_fileid, upload_file.name,1,0,upload_file.size)
            CITaskService.update_ci_taskhistory(tq_id,result,file_type)
        return result
    
    @staticmethod
    def download_package(request,file_path):
        return PackgeMongoFile.objects.get(file_path)

    
    @staticmethod
    def update_property(request,taskid):
        task=CITask.objects.get(taskid)
        task.Tags=request.POST.get("Tags")
        update_fields=list()
        for field in request.POST:
            update_fields.append(field)
        task.save(update_fields=update_fields)
        CITaskService.log_change_activity(request.user,task)
    
    @staticmethod
    def get_avalible_menu_tags(menu_type):
        '''
           menu_type: 1: ci_task,2:task_history,3:agent
        '''
        tag_types=[1]
        if str(menu_type)=="1":
            tag_types=[1,4]
        
        if str(menu_type)=="2":
            tag_types=[2]
            
        if str(menu_type)=="3":
            tag_types=[3]
        
        if str(menu_type)=="4":
            tag_types=[4]
        return Tag.objects.all().filter(TagType__in=tag_types)
    
    @staticmethod
    def get_agent_filter__tags():
        return Tag.objects.all().filter(TagType__in=[3])
    
           
    

    @staticmethod
    def log_create_activity(user,ci_task):
        CITask.objects.log_action(user.id,ci_task.id,ci_task.TaskName,ADDITION,"创建了CI任务",ci_task.Project,CITaskService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,ci_task):
        CITask.objects.log_action(user.id,ci_task.id,ci_task.TaskName,DELETION,"删除了CI任务",ci_task.Project,CITaskService.ActionLogType.CI)
    
    @staticmethod
    def log_clean_activity(user,ci_task):
        CITask.objects.log_action(user.id,ci_task.id,ci_task.TaskName,DELETION,"删除了历史记录",ci_task.Project,CITaskService.ActionLogType.CI)
    
    
    @staticmethod
    def log_change_activity(user,ci_task):
        CITask.objects.log_action(user.id,ci_task.id,ci_task.TaskName,CHANGE,"修改了CI任务",ci_task.Project,CITaskService.ActionLogType.CI)
    
    @staticmethod
    def log_build_activity(user_id,ci_task):
        CITask.objects.log_action(user_id,ci_task.id,ci_task.TaskName,CHANGE,"构建了CI任务",ci_task.Project,CITaskService.ActionLogType.CI)
        
        
        
        
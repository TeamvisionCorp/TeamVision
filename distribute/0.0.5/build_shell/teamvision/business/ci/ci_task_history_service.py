#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from business.business_service import BusinessService
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from business.common.redis_service import RedisService
from business.common.mongodb_service import MongoDBService
from teamvision.api.ci.mongo_models import BuildLogMongoFile,PackgeMongoFile,ReleaseArchiveMongoFile
from business.common.file_info_service import FileInfoService
from teamvision.ci.models import CITaskHistory,CITask,CITaskStepOutput,CITaskStageHistory,AutoTestingTaskResult,AutoCaseResult
from teamvision.home.models import FileInfo,TaskQueue
from teamvision.project.models import ProjectArchive
from business.common.system_config_service import SystemConfigService
from business.ci.ci_task_config_service import CITaskConfigService

import threading
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.settings import WEB_HOST,ROOT_DIR
import os,shutil


class CITaskHistoryService(BusinessService):
    '''
    classdocs
    '''
    
    @staticmethod
    def save_build_log(tq_id,tq_done=False):
        file_name="ci_build_log"+tq_id+".log"
        build_log=RedisService.get_value("ci_build_log"+tq_id)
        result=MongoDBService.save_content_asfile(file_name, build_log,BuildLogMongoFile)
        file_id=FileInfoService.add_file(0,result,file_name,1,0,len(build_log))
        RedisService.delete_value("ci_build_log" + tq_id)
        if tq_done:
            temp_output = CITaskStepOutput()
            temp_output.ProductType = 1
            temp_output.ProductID = file_id
            task_queue = TaskQueue.objects.get(int(tq_id))
            task_history = CITaskHistory.objects.get_history_by_uuid(task_queue.TaskUUID)
            temp_output.TaskHistoryID = task_history.id
            temp_output.TaskID = task_history.CITaskID
            temp_output.StepID = ""
            temp_output.StageHistoryID = 0
            temp_output.save()
        else:
            RedisService.set_value("ci_build_log"+tq_id,"")
        return file_id

    @staticmethod
    def archive_release_package(history_id):
        release_history=CITaskHistory.objects.get(int(history_id))
        if release_history:
            new_file_ids=CITaskHistoryService.copy_package(release_history)
        return new_file_ids

    
    
                   
    @staticmethod
    def copy_package(history):
        '''
          copy release package to release resp
        '''
        result=list()
        if history.PackageID and not CITaskHistoryService.is_history_archived(history) :
            history_files=list()
            new_archive=CITaskHistoryService.new_archive(history,history_files)
            for old_file_id in eval(history.PackageID):
                file_id=0
                try:
                    file_id=FileInfoService.copy_file(old_file_id,PackgeMongoFile,ReleaseArchiveMongoFile)
                    result.append(file_id)
                    history_files.append(file_id)
                except Exception as ex:
                    FileInfoService.delete_file(file_id, ReleaseArchiveMongoFile)
                    new_archive.delete()
                    SimpleLogger.exception(ex)
                    result=None
            
            if result:
                file_ids=""
                for file_id in history_files:
                    file_ids=file_ids+str(file_id)+","
                new_archive.Archives=file_ids
                new_archive.save()
        return result
    
    
    @staticmethod
    def new_archive(history,new_file_ids):
        ci_task=CITask.objects.get(history.CITaskID)
        temp_archive=ProjectArchive()
        temp_archive.VersionID=history.ProjectVersion
        temp_archive.ProjectID=ci_task.Project
        temp_archive.HistoryID=history.id
        file_ids=""
        temp_archive.Archives=file_ids
        temp_archive.save()
        return temp_archive
    
    @staticmethod
    def is_history_archived(history):
        archives=ProjectArchive.objects.all().filter(HistoryID=history.id)
        if len(archives)>0:
            return True
        else:
            return False
        
    
    
    @staticmethod
    def remove_history_tag(history_list,tag):
        '''
            remove tag form history
        '''
        for history in history_list:
            try:
                history.Tags=history.Tags.replace(str(tag)+",","")
                history.save()
            except Exception as ex:
                SimpleLogger.exception(ex)
                continue
        
                    
    
    @staticmethod
    def get_release_history(project_id,version_id):
        result=list()
        ci_task_list=CITask.objects.project_tasks(project_id).filter(TaskType=4)
        for task in ci_task_list:
            history_list=CITaskHistory.objects.get_task_history(task.id)
            if history_list:
                for history in history_list.filter(ProjectVersion=version_id):
                    if history.Tags:
                        if 13 in eval(history.Tags):
                            result.append(history)
        return result
    
    @staticmethod
    def remove_build_history(task_id):
        current_task=CITask.objects.get(task_id)
        start_index=current_task.HistoryCleanStrategy
        task_historys=CITaskHistory.objects.get_task_history(task_id,is_active=0).order_by('-id')[start_index:]
        for history in task_historys:
            history.IsActive = 0
            history.save()


    @staticmethod
    def clean_build_history(history_id):
        history = CITaskHistory.objects.get(int(history_id),is_active=0)
        stage_histories = CITaskStageHistory.objects.get_sthistory_bythistory_id(int(history_id))
        for stage_history in stage_histories:
            CITaskHistoryService.delete_output(stage_history.id)
            CITaskHistoryService.delete_test_results(stage_history.id)
            stage_history.delete()
        history.delete()




    @staticmethod
    def delete_test_results(stage_historyid):
        try:
            test_results = AutoTestingTaskResult.objects.get_by_historyid(int(stage_historyid))
            for result in test_results:
                case_results = AutoCaseResult.objects.get_by_resultid(result.id,0)
                case_results.delete()
                result.delete()
        except Exception as ex:
            SimpleLogger.exception(ex)

    @staticmethod
    def delete_output(stage_historyid):
        try:
            outputs = CITaskStepOutput.objects.get_stage_output(int(stage_historyid))
            for output in outputs:
                if output.ProductID:
                    if output.ProductType in (2,3,6):
                        FileInfoService.delete_file(output.ProductID)
                        CITaskHistoryService.clean_temp_file(output.ProductID)
                    if output.ProductType == 1:
                        FileInfoService.delete_file(output.ProductID,mongo_model=BuildLogMongoFile)
                        CITaskHistoryService.clean_temp_file(output.ProductID)
                    if output.ProductType == 5:
                        PackgeMongoFile.objects.delete_value(output.ProductID)
                output.delete()
        except Exception as ex:
            SimpleLogger.exception(ex)





    
    
    @staticmethod
    def clean_all_history(task_id,task_delete):
        task_historys=CITaskHistory.objects.get_task_history(int(task_id),is_active=0)
        if not task_delete:
            task_historys=task_historys.filter(Tags__isnull=True)
        worker=threading.Thread(target=CITaskHistoryService.history_clean_worker,args=(task_historys,))
        worker.start()
        
            
    @staticmethod
    def history_clean_worker(task_historys):
        for history in task_historys:
            try:
                if history.PackageID:
                    for fileid in eval(history.PackageID):
                        FileInfoService.delete_file(fileid)
                        CITaskHistoryService.clean_temp_file(fileid)
                if history.LogFileID:
                    for fileid in eval(history.LogFileID):
                        FileInfoService.delete_file(fileid)
                        CITaskHistoryService.clean_temp_file(fileid)
                        
                if history.BuildLogID:
                    FileInfoService.delete_file(history.BuildLogID,mongo_model=BuildLogMongoFile)
                    history.BuildLogID=0
                
                if history.ChangeLog:
                    PackgeMongoFile.objects.delete_value(history.ChangeLog)
                history.IsActive=0
            except Exception as ex:
                SimpleLogger.exception(ex)
                history.IsActive=1
                continue
            finally:
                history.save()
    
    @staticmethod
    def clean_temp_file(file_id):
        try:
            ipa_file_path=(ROOT_DIR+"/"+"static/ipa_files/"+str(file_id)+".ipa").replace("\\","/")
            plist_file_path=ROOT_DIR+"/"+"static/plist_files/"+str(file_id)+".plist"
            if os.path.exists(ipa_file_path):
                os.remove(ipa_file_path)
        
            if os.path.exists(plist_file_path):
                os.remove(plist_file_path)
        except Exception as ex:
            SimpleLogger.exception(ex)
            
    
    @staticmethod
    def save_change_log(change_log):
        result=dict()
        result['change_log']=change_log
        mongo_id=MongoDBService.save("teamcat_log","code_changelog",result)
        return mongo_id
    
    @staticmethod
    def get_change_log(change_log_id):
        value=MongoDBService.get("teamcat_log","code_changelog",change_log_id)
        return value
    
    @staticmethod
    def get_finished_history(task_id):
        dm_task_histories=CITaskHistory.objects.get_task_history(int(task_id)).order_by('-id')
        return dm_task_histories
        
    
    @staticmethod
    def get_build_log(file_id):
        file=FileInfo.objects.get(int(file_id))
        contents=BuildLogMongoFile.objects.get(file.FilePath)
        return contents
    
    @staticmethod
    def get_big_build_log(file_id):
        file=FileInfo.objects.get(int(file_id))
        contents=BuildLogMongoFile.objects.get(file.FilePath)
        return contents
    

    
    @staticmethod
    def format_build_log(contents):
        result=""
        if "{ENTER}" in contents:
            build_logs=contents.split('{ENTER}')
            for log in build_logs:
                if "[ERROR]" in log.upper():
                    result=result+"</br>"+"<strong style='color:red;font-size:18px;'>"+log.replace('{ENTER}','</br>')+"</strong>"
                else:
                    result=result+"</br>"+log.replace('{ENTER}','</br>')         
        else:
            result=contents
        return result
        
    
    @staticmethod
    def get_latest_codeversion(task_id):
        result=None
        historys=CITaskHistory.objects.all().filter(CITaskID=task_id).order_by('-id')
        return result

    @staticmethod
    def upload_package(request):
        result = None
        upload_file = request.FILES['upload_file']
        max_file_size = SystemConfigService.get_upload_file_maxsize()
        file_wihte_list = SystemConfigService.get_file_type_white_list()
        if CITaskHistoryService.validate_upload_file(upload_file, max_file_size, file_wihte_list):
            mongo_fileid = MongoDBService.save_file(upload_file, PackgeMongoFile)
            file_id = FileInfoService.add_file(0, mongo_fileid, upload_file.name, 1, 0, upload_file.size)
            temp_output = CITaskStepOutput()
            temp_output = CITaskHistoryService.init_step_output(temp_output,request.data)
            temp_output.ProductID = file_id
            temp_output.save()
            result = temp_output
        return result

    @staticmethod
    def save_step_log(request_data):
        print(request_data)
        output_id = request_data.get("id",None)
        if output_id is None:
            temp_output = CITaskStepOutput()
            temp_output = CITaskHistoryService.init_step_output(temp_output,request_data)
        else:
            temp_output = CITaskStepOutput.objects.get(output_id)
            temp_output = CITaskHistoryService.init_step_output(temp_output, request_data)
            task_history = CITaskHistory.objects.get(temp_output.TaskHistoryID)
            task_queue = TaskQueue.objects.get_byUUID(task_history.TaskUUID)
            temp_output.ProductID = CITaskHistoryService.save_build_log(str(task_queue.id))
        temp_output.ProductType = 1
        temp_output.save()
        return temp_output


    @staticmethod
    def get_log_content(output,show_content):
        temp_output = dict()
        temp_output["id"] = output.id
        task_step = CITaskConfigService.task_step(output.StepID)
        if task_step:
            temp_output["step_name"] = str(task_step.step_config["step_name"]) + " " + str(task_step.purpose_name)
        else:
            temp_output["step_name"] = "--"
        log_file = FileInfo.objects.get(output.ProductID)
        if (log_file is not None and log_file.FileSize<512) or show_content:
            contents = CITaskHistoryService.get_big_build_log(output.ProductID)
            c = contents.read()
            log_content = c.decode('utf-8').replace("base", "")
            log_content = CITaskHistoryService.format_build_log(log_content)
            temp_output["log_content"] = log_content
            temp_output["show_content"] = True
        else:
            temp_output["log_content"] = "日志内容较多，请手动加载"
            temp_output["show_content"] = False
        return temp_output


    @staticmethod
    def init_step_output(output,request_data):
        if output is not None:
            output.StageID = request_data.get("StageID", None)
            output.TaskID = request_data.get("TaskID", None)
            output.StageHistoryID = request_data.get("StageHistoryID", None)
            output.StepID = request_data.get("StepID", None)
            output.TaskHistoryID = request_data.get("TaskHistoryID", None)
            output.ProductType = request_data.get("ProductType",1)
        return output



        
        
        
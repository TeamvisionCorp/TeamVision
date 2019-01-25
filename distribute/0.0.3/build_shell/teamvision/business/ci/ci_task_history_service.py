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
from teamvision.ci.models import CITaskHistory,CITask
from teamvision.home.models import FileInfo
from teamvision.project.models import ProjectArchive
import threading
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.settings import WEB_HOST,ROOT_DIR
import os,shutil


class CITaskHistoryService(BusinessService):
    '''
    classdocs
    '''
    
    @staticmethod
    def save_build_log(tq_id):
        file_name="ci_build_log"+tq_id+".log"
        build_log=RedisService.get_value("ci_build_log"+tq_id)
        result=MongoDBService.save_content_asfile(file_name, build_log,BuildLogMongoFile)
        file_id=FileInfoService.add_file(0,result,file_name,1,0,len(build_log))
        task_history=CITaskHistory.objects.get_by_tqid(int(tq_id))
        if file_id:
            task_history.BuildLogID=file_id
        else:
            task_history.BuildLogID=0
        task_history.save() 
    

    @staticmethod
    def archive_release_package(history_id):
        release_history=CITaskHistory.objects.get(int(history_id))
        if release_history:
            new_file_ids=CITaskHistoryService.copy_package(release_history)
# if copy file success, remove release tag from ci history
#         if new_file_ids!=None:
#             CITaskHistoryService.remove_history_tag(release_history,13)
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
    def clean_build_history(history_id):
        task_history=CITaskHistory.objects.get(int(history_id),is_active=0)
        current_task=CITask.objects.get(task_history.CITaskID)
        start_index=current_task.HistoryCleanStrategy
        task_historys=CITaskHistory.objects.get_task_history(task_history.CITaskID,is_active=0).filter(Tags__isnull=True).order_by('-id')[start_index:]
        worker=threading.Thread(target=CITaskHistoryService.history_clean_worker,args=(task_historys,))
        worker.start()
    
    
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
    def get_build_log(request,file_id):
        file=FileInfo.objects.get(int(file_id))
        contents=BuildLogMongoFile.objects.get(file.FilePath)
        return contents
    
    @staticmethod
    def get_big_build_log(request,file_id):
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
        if historys:
            for history in historys:
                if history.CodeVersion:
                    result=history.CodeVersion
                    break
        return result
        
        
        
        
        
        
#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''

from teamvision.ci.models import CITask
from business.auth_user.user_service import UserService
from teamvision.ci.viewmodels.vm_ci_build_file import VM_CIBuildFile
from business.ci.ci_task_history_service import CITaskHistoryService
from business.ci.ci_task_parameter_service import CITaskParameterService
from teamvision.ci.viewmodels.vm_ci_task_changelog import VM_CITaskChangeLog
from teamvision.project.models import Version,Project
from teamvision.project.models import Tag
from teamvision.home.models import FileInfo
from json.decoder import JSONDecoder
from teamvision.home.models import Agent
from gatesidelib.common.simplelogger import SimpleLogger


class VM_CITaskHistory(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_ci_task_history,tag_menu):
        self.ci_task_history=dm_ci_task_history
        self.ci_task=self.get_ci_task()
        self.started_by=self.started_by()
        self.tag_menu=tag_menu
        
    def get_ci_task(self):
        return CITask.objects.get(self.ci_task_history.CITaskID)
    
    
    
    def project_name(self):
        project=Project.objects.get(self.ci_task.Project)
        return project.PBTitle
    
    
    @property
    def last_run_time(self):
        result="未能成功执行"
        if self.ci_task_history.StartTime:
            result=self.ci_task_history.StartTime
        return result
    
    @property
    def build_log_is_big(self):
        result=False
        if self.ci_task_history.BuildLogID:
            build_log_file=FileInfo.objects.get(self.ci_task_history.BuildLogID)
            if build_log_file.FileSize!=None:
                result=(build_log_file.FileSize/1024)>10
        return result
        
    
    @property
    def duration(self):
        result="--"
        if self.ci_task_history.StartTime and self.ci_task_history.EndTime:
            durations=(self.ci_task_history.EndTime-self.ci_task_history.StartTime).total_seconds()
            result=int(durations/60)
            if result==0:
                result=str(durations)+"秒"
            else:
                result=str(result)+"分钟"
        return result
    
    @property
    def version(self):
        result="--"
        if self.ci_task_history.ProjectVersion:
            result=Version.objects.get(self.ci_task_history.ProjectVersion).VVersion
        return result
    
    @property
    def bound_version(self):
        result=""
        try:
            if self.ci_task_history.PackageInfo:
                result="("+eval(self.ci_task_history.PackageInfo)['version']+")"
        except Exception as ex:
            SimpleLogger.error(ex)
        return result
    
    @property
    def task_tags(self):
        result=list()
        if self.ci_task_history.Tags:
            for tag_id in eval(self.ci_task_history.Tags):
                tmp_tag=Tag.objects.get(tag_id)
                if tmp_tag:
                    result.append(tmp_tag)              
        return result
    
    @property
    def build_parameter(self):
        result="--"
        if self.ci_task_history.BuildParameterID:
            parameter_group=CITaskParameterService.task_parameter(self.ci_task_history.BuildParameterID)
            if parameter_group:
                result=parameter_group.group_name
        return result
    
    @property
    def agent_name(self):
        result="--"
        if self.ci_task_history.AgentID!=0:
            agent=Agent.objects.get(self.ci_task_history.AgentID)
            if agent:
                result=agent.Name
        return result
    
    @property
    def has_parameter(self):
        return self.ci_task_history.BuildParameterID!=None
        
    
    
    @property
    def change_logs(self):
        result=list()
        try:
            change_logs=CITaskHistoryService.get_change_log(self.ci_task_history.ChangeLog)
            json_decoder=JSONDecoder()
            if change_logs:
                all_resp_changes=json_decoder.decode(change_logs['change_log'])
                index=1
                for resp_changes in all_resp_changes:
                    repo=resp_changes['repo']
                    for changes in resp_changes['changes']:
                        temp_changelog=VM_CITaskChangeLog(changes,index,repo)
                        result.append(temp_changelog)
                        index=index+1
            elif self.ci_task_history.CodeVersion:
                all_changes=json_decoder.decode(self.ci_task_history.CodeVersion)
                temp_changelog=VM_CITaskChangeLog(all_changes[0],0, "")
                result.append(temp_changelog)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def started_by(self):
        result=None
        if self.ci_task_history.StartedBy:
            result=UserService.get_user(self.ci_task_history.StartedBy)
        return result
    
    def started_by_avatar(self):
        result="/static/global/images/caton/caton1.jpeg"
        if self.started_by:
            if self.started_by.extend_info.avatar.isdigit():
                avatar_path=FileInfo.objects.get(int(self.started_by.extend_info.avatar))
                result="/ucenter/account/get_avatar/"+avatar_path.FilePath
            else:
                result=self.started_by.extend_info.avatar
        return result
    
    def started_by_name(self):
        result="系统任务"
        if self.started_by:
            result=self.started_by.last_name+self.started_by.first_name
        return result
    
    def build_package(self):
        package_list=list()
        if self.ci_task_history.PackageID:
            for file_id in eval(self.ci_task_history.PackageID):
                temp_package=VM_CIBuildFile(file_id,self.ci_task_history.id)
                package_list.append(temp_package)
        return package_list
    
    def has_package(self):
        return self.ci_task_history.PackageID!=None
                
    
    def log_package(self):
        log_file_list=list()
        if self.ci_task_history.LogFileID:
            for file_id in eval(self.ci_task_history.LogFileID):
                temp_package=VM_CIBuildFile(file_id,self.ci_task_history.id)
                log_file_list.append(temp_package)
        return log_file_list
        
    
    
    def is_build_success(self):
        result="status-background-default"
        if self.ci_task_history.BuildStatus==1:
            result="status-background-success"
        if self.ci_task_history.BuildStatus==2:
            result="status-background-fail"
        if self.ci_task_history.BuildStatus==3:
            result="status-background-cancel"
        return result
    
    def is_build_success_color(self):
        result="status-default"
        if self.ci_task_history.BuildStatus==1:
            result="status-success"
        if self.ci_task_history.BuildStatus==2:
            result="status-fail"
        if self.ci_task_history.BuildStatus==3:
            result="status-cancel"
        return result
    
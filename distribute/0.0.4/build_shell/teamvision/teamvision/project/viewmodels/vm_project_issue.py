#coding=utf-8
'''
Created on 2015-11-9

@author: Devuser
'''
from teamvision.project.models import Project,ProjectModule,ProjectOS
from teamvision.project.models import Version,ProjectIssueSeverity,ProjectIssueStatus,ProjectIssueResolvedResult
from teamvision.project.models import ProjectPhase,ProjectIssueCategory,ProjectOSVersion,ProjectIssue
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService
from business.auth_user.user_service import UserService
from teamvision.home.models import FileInfo
from teamvision.home.viewmodels.vm_file_info import VM_FileInfo
from gatesidelib.datetimehelper import DateTimeHelper
from teamvision.home.models import Team
import time,datetime,pytz
from teamvision.gatesidelib.common.simplelogger import SimpleLogger

class VM_ProjectIssue(object):
    



    def __init__(self,user_id,issue):
        '''
        Constructor
        '''
        self.issue=issue
        self.user_id=user_id
        
    
    
    def project_title(self):
        dm_project=Project.objects.get(self.issue.Project)
        return dm_project.PBTitle
    
    def default_title(self):
        if str(self.issue.Team):
            default_title="["+self.team_name() +" "+self.project_title()+" "+self.version()+" "+self.module_name()+"]"
        return default_title
   
    
    def os_name(self):
        result=" "
        try:
            if self.issue.DeviceOS:
                result=ProjectOS.objects.get_byvalue(self.issue.DeviceOS).Name
        except Exception as ex:
            SimpleLogger.exception(ex)
    
        return result
    def os_version(self):
        return ProjectOSVersion.objects.get_byvalue(self.issue.DeviceOS,self.issue.OSVersion)
    
    def module_name(self):
        result=" "
        if self.issue.Module:
            dm_module=ProjectModule.objects.get(self.issue.Module)
            result=dm_module.Name
        return result

    def team_name(self):
        result=""
        if self.issue.Team:
            dm_team=Team.objects.get(self.issue.Team)
            result=dm_team.Name
        return result
    
    def version(self):
        result=""
        dm_version=Version.objects.get(self.issue.Version)
        if dm_version:
            result=dm_version.VVersion
        return result
    
    def issue_temp_id(self):
        return str(self.user_id)+"_"+str(time.time())
    
    def severity(self):
        return ProjectIssueSeverity.objects.get_byvalue(self.issue.Severity)
    
    def status(self):
        return ProjectIssueStatus.objects.get_byvalue(self.issue.Status)
    
    def solution(self):
        return ProjectIssueResolvedResult.objects.get_byvalue(self.issue.Solution)
    
    def category(self):
        return ProjectIssueCategory.objects.get_byvalue(self.issue.IssueCategory)
    
    def project_phase(self):
        return ProjectPhase.objects.get_byvalue(self.issue.ProjectPhase)
        
    
    
    def creator_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        try:
            creator=User.objects.get(id=self.fortesting.Creator)
            if creator.extend_info:
                result=AccountService.get_avatar_url(creator)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def creator_name(self):
        creator=User.objects.get(id=self.issue.Creator)
        result=creator.username
        if creator.first_name and creator.last_name:
            result=creator.last_name+creator.first_name
        return result
    
    def processor_name(self):
        processor=User.objects.get(id=self.issue.Processor)
        result=processor.username
        if processor.first_name and processor.last_name:
            result=processor.last_name+processor.first_name
        return result
    
    def create_date(self):
        result="--"
        if self.issue.CreationTime:
            result=self.issue.CreationTime
        return result

    def update_date(self):
        result="--"
        if self.issue.ResolvedTime:
            result=DateTimeHelper.how_long_ago((datetime.datetime.now().replace(tzinfo=pytz.timezone('Asia/Shanghai'))-self.issue.ResolvedTime).seconds)
        return result
    
    def attachments(self):
        result=list()
        if self.issue.Attachments:
            for file_id in eval(self.issue.Attachments):
                file=FileInfo.objects.get(int(file_id))
                if file.IsActive!=0:
                    temp_file=VM_FileInfo(file)
                    result.append(temp_file)
        return result
    
            
        
    def testing__finished_date(self):
        result="--"
        if self.fortesting.TestingFinshdedDate:
            result=self.fortesting.TestingFinshdedDate
        return result
    
    
        
    def testing_deadline(self):
        result="--"
        if self.fortesting.TestingDeadLineDate:
            result=self.fortesting.TestingDeadLineDate
        return result
    
    def fortesting_attachments(self):
        result=list()
        try:
            if self.fortesting.Attachment!=None and self.fortesting.Attachment.strip()!="":
                for file_id in eval(self.fortesting.Attachment):
                    file=FileInfo.objects.get(int(file_id))
                    temp_file=VM_FileInfo(file)
                    result.append(temp_file)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def has_attachments(self):
        result=False
        if self.fortesting.Attachment!=None:
            result=True
        return result
    
    
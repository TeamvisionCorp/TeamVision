#coding=utf-8
'''
Created on 2015-11-9

@author: Devuser
'''
from teamvision.project.models import Project,ProjectModule,ProjectCodeUrl
from teamvision.project.models import Version
from teamvision.project.viewmodels.vm_project_fortesting_tester import VM_FortestingTester
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService
from business.auth_user.user_service import UserService
from teamvision.home.models import FileInfo
from teamvision.home.viewmodels.vm_file_info import VM_FileInfo
from gatesidelib.datetimehelper import DateTimeHelper
from teamvision.gatesidelib.common.simplelogger import SimpleLogger
import datetime

class VM_ProjectForTesting(object):
    



    def __init__(self,fortesting,is_create=False):
        '''
        Constructor
        '''
        self.fortesting=fortesting
        self.is_create=is_create
    
    def is_commited(self):
        result=False
        if self.fortesting.Status==2:
            result=True
        return result
    
    def project_title(self):
        dm_project=Project.objects.get(self.fortesting.ProjectID)
        return dm_project.PBTitle
    
    def module_name(self):
        dm_project=Project.objects.get(self.fortesting.ProjectID)
        dm_module=ProjectModule.objects.get(dm_project.ProjectModuleID)
        return dm_module.Name
    
    def has_module(self):
        dm_project=Project.objects.get(self.fortesting.ProjectID)
        if dm_project.PBPlatform  in (4,6,7):
            return True
        else:
            return False
    
    def version(self):
        result=""
        dm_version=Version.objects.get(self.fortesting.VersionID)
        if dm_version:
            result=dm_version.VVersion
        return result
    
    def platform(self):
        result="fa-android"
        project=Project.objects.get(self.fortesting.ProjectID)
        if project.PBPlatform==1:
            result="fa-android"
         
        if project.PBPlatform==2:
            result="fa-windows"
         
        if project.PBPlatform==3:
            result="fa-apple"
        if project.PBPlatform==4:
            result="fa-chrome"
        
        return result
    
    def form_id(self):
        if self.is_create:
            return "fortesting-create-form"
        else:
            return "fortesting-edit-form"
        
    def commitor_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        commitor=User.objects.get(id=self.fortesting.Commitor)
        if commitor.extend_info:
            result=AccountService.get_avatar_url(commitor)
        return result
    
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
        creator=User.objects.get(id=self.fortesting.Creator)
        result=creator.username
        if creator.first_name and creator.last_name:
            result=creator.last_name+creator.first_name
        return result
    
    
    def commitor_name(self):
        result="--"
        if self.fortesting.Commitor:
            commitor=User.objects.get(id=self.fortesting.Commitor)
            if commitor.first_name and commitor.last_name:
                result=commitor.last_name+commitor.first_name
        if len(result)>2:
            return result[1:]
        else:
            return result
    
    def code_resp(self):
        result=""
        if self.fortesting.ProjectCode and self.fortesting.ProjectCode!=0:
            project_code=ProjectCodeUrl.objects.get(self.fortesting.ProjectCode)
            result=project_code.CodeRepertory
        return result
    
    def code_branch(self):
        result=""
        if self.fortesting.ProjectCode and self.fortesting.ProjectCode!=0:
            project_code=ProjectCodeUrl.objects.get(self.fortesting.ProjectCode)
            result=project_code.Branch
        return result
    
    def topic(self):
        result=""
        if self.fortesting.Topic:
            result=self.fortesting.Topic
        else:
            result=self.fortesting.TestingFeature
        return result
    
    def has_code_resp(self):
        result=False
        if self.fortesting.ProjectCode and self.fortesting.ProjectCode!=0:
            result=True
        return result
    
    def fortesting_testers(self):
        users=list()
        for testerid in eval(self.fortesting.Testers):
            user=UserService.get_user(testerid)
            if user!=None:
                tmp_user=VM_FortestingTester(0,user,None,None,self.fortesting)
                users.append(tmp_user)
        return users
    
    def commit_date(self):
        result="--"
        if self.fortesting.CommitTime:
            result=self.fortesting.CommitTime
        return result
    
    def testing_start_date(self):
        result="--"
        if self.fortesting.TestingStartDate:
            result=self.fortesting.TestingStartDate
        else:
            result=DateTimeHelper.get_now_date()
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
    
    def worker_name(self):
        result="--"
        worker_id=0
        if self.fortesting.Status==1:
            worker_id=self.fortesting.Creator
        if self.fortesting.Status==2:
            worker_id=self.fortesting.Commitor
        if self.fortesting.Status==3:
            worker_id=self.fortesting_testers()[0].member.id
        if self.fortesting.Status==4:
            worker_id=self.fortesting_testers()[0].member.id
        if self.fortesting.Status==5:
            worker_id=self.fortesting_testers()[0].member.id
        if worker_id!=0:
            commitor=User.objects.get(id=worker_id)
            if commitor.first_name and commitor.last_name:
                result=commitor.last_name+commitor.first_name
        if len(result)>2:
            return result[1:]
        else:
            return result
        return result    
    
       
    def expect_commit_date(self):
        result="明天"
        if self.fortesting.Status==1:
            expect_date=self.fortesting.CreationTime
        if self.fortesting.Status==2:
            expect_date=self.fortesting.CommitTime
        if self.fortesting.Status==3:
            expect_date=self.fortesting.TestingDeadLineDate
        if self.fortesting.Status==4:
            expect_date=self.fortesting.TestingFinishedDate
        if self.fortesting.Status==5:
            expect_date=self.fortesting.TestingFinishedDate
        
        if expect_date!=None:
            expect_date=expect_date+datetime.timedelta(hours=8)
            action_time=datetime.datetime.strptime(expect_date.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            data_interval=DateTimeHelper.get_time_to_now(str(action_time),"%Y-%m-%d %H:%M:%S")
            result=DateTimeHelper.how_long_tonow(data_interval)
        return result
        
        
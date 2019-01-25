#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from model_managers.model_manager import ModelManager


class TaskManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(TaskManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,taskid):
        result=None
        try:
            result=super(TaskManager,self).get_queryset().get(id=taskid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_tasks(self,project_id):
        result=list()
        try:
            result=self.all().filter(ProjectID=project_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_child_tasks(self,task_id,status=-1):
        result=list()
        try:
            if status<0:
                result = self.all().filter(Parent=int(task_id))
            else:
                result = self.all().filter(Parent=int(task_id)).filter(Status=int(status))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class VersionManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(VersionManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,versionid):
        result=None
        try:
            result=super(VersionManager,self).get_queryset().get(id=versionid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_versions(self,project_id):
        result=list()
        try:
            result=self.all().filter(VProjectID=project_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
class TestApplicationManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(TestApplicationManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,tp_id):
        result=None
        try:
            result=super(TestApplicationManager,self).get_queryset().get(id=tp_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def project_fortestings(self,project_id):
        result=list()
        try:
            result=self.all().filter(ProjectID= project_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    

class WebHookManager(ModelManager):
    '''
    classdocs
    '''
    def all(self,project_id):
        
        return super(WebHookManager,self).get_queryset().filter(WHProjectID=project_id).filter(IsActive=1)
    
    def get(self,webhook_id):
        result=None
        try:
            result=super(WebHookManager,self).get_queryset().get(id=webhook_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_build_webhook(self,project_id):
        result=None
        try:
            result=super(WebHookManager,self).get_queryset().all().filter(WHProjectID=project_id).filter(WHCatagory=1).filter(WHIsDefault=1)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
        
class BuildHistoryManager(ModelManager):
    '''
    classdocs
    '''

class CodeUrlManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(CodeUrlManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,code_url_id):
        result=None
        try:
            result=super(CodeUrlManager,self).get_queryset().get(id=code_url_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class MemberManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(MemberManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,memberid):
        result=None
        try:
            result=super(MemberManager,self).get_queryset().get(id=memberid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_members(self,projectid):
        return self.all().filter(PMProjectID=projectid)
    
    def get_member(self,projectid,userid):
        result=None
        try:
            result=self.get_members(projectid).filter(PMMember=userid)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class TagManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(TagManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,tagid):
        result=None
        try:
            result=super(TagManager,self).get_queryset().get(id=tagid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def has_tag(self,tag_name):
        result=super(TagManager,self).get_queryset().filter(TagName=tag_name)
        if len(result)>0:
            return True
        else:
            return False


class ProjectManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(ProjectManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,projectid):
        result=None
        try:
            result=super(ProjectManager,self).get_queryset().get(id=projectid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def check_value_exits(self,filed_name,filed_value):
        result=None
        try:
            if filed_name=="PBTitle":
                result=self.all().filter(PBTitle=filed_value)
            if filed_name=="PBKey":
                result=self.all().filter(PBKey=filed_value)
                
        except Exception as ex:
            SimpleLogger.exception(ex)
        if len(result)==0:
            return False
        else:
            return True
        

class RoleManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(RoleManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,projectid):
        result=None
        try:
            result=super(RoleManager,self).get_queryset().get(id=projectid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class ArchiveManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(ArchiveManager,self).get_queryset().filter(IsActive=1)
    
    
    def get_project_archives(self,projectid):
        result=None
        try:
            result=super(ArchiveManager,self).get_queryset().filter(ProjectID=projectid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_version_archives(self,version_id):
        result=None
        try:
            result=super(ArchiveManager,self).get_queryset().filter(VersionID=version_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get(self,archive_id):
        result=None
        try:
            result=super(ArchiveManager,self).get_queryset().filter(id=archive_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    


class IssueManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(IssueManager,self).get_queryset().filter(IsActive=1)
    
    
    def get_project_issue(self,projectid):
        result=None
        try:
            result=self.all().filter(Project=projectid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_version_issue(self,version_id):
        result=None
        try:
            result=self.all().filter(Version=version_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_processor_issue(self,processor_id):
        result=None
        try:
            result=self.all().filter(Processor=processor_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_reporter_issue(self,reporter_id):
        result=None
        try:
            result=self.all().filter(Creator=reporter_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get(self,issue_id):
        result=None
        try:
            result=super(IssueManager,self).get_queryset().get(id=issue_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result




class IssueDailyStatisticsManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(IssueDailyStatisticsManager,self).get_queryset().filter(IsActive=1)
    
    
    def get_project_issue_statistics(self,projectid):
        result=None
        try:
            result=self.all().filter(ProjectID=projectid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_version_issue_statistics(self,version_id):
        result=None
        try:
            result=self.all().filter(VersionID=version_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    
    def get(self,issue_id):
        result=None
        try:
            result=super(IssueDailyStatisticsManager,self).get_queryset().get(id=issue_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class IssueVersionStatisticsManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(IssueVersionStatisticsManager,self).get_queryset().filter(IsActive=1)
    
    
    def get_project_issue_statistics(self,projectid):
        result=None
        try:
            result=self.all().filter(ProjectID=projectid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_version_issue_statistics(self,version_id):
        result=None
        try:
            result=self.all().filter(VersionID=version_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    
    def get(self,issue_id):
        result=None
        try:
            result=super(IssueVersionStatisticsManager,self).get_queryset().get(id=issue_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result



class IssueConfigFieldManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(IssueConfigFieldManager,self).get_queryset().filter(IsActive=1)
    
    
    def get_byvalue(self,config_value):
        result=None
        try:
            result=super(IssueConfigFieldManager,self).get_queryset().filter(Value=config_value)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class ProjectOSVersionManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(ProjectOSVersionManager,self).get_queryset().filter(IsActive=1)
    
    
    def get_byvalue(self,os,config_value):
        result=None
        try:
            result=super(ProjectOSVersionManager,self).get_queryset().filter(Value=config_value).filter(OS=os)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_by_os(self,os_value):
        result=None
        try:
            result=super(ProjectOSVersionManager,self).get_queryset().filter(OS=os_value)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result



class ProductManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(ProductManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,productid):
        result=None
        try:
            result=super(ProductManager,self).get_queryset().get(id=productid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class ModuleManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(ModuleManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,moduleid):
        result=None
        try:
            result=super(ModuleManager,self).get_queryset().get(id=moduleid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    def project_modules(self,project_id):
        result=None
        try:
            result=self.all().filter(ProjectID=project_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class IssueActivityManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(IssueActivityManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,activity_id):
        result=None
        try:
            result=super(IssueActivityManager,self).get_queryset().get(id=activity_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    def issue_activity(self,issue_id):
        result=None
        try:
            result=self.all().filter(Issue=issue_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
class IssueFilterManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(IssueFilterManager,self).get_queryset().filter(IsActive=1)
    
    
    def get(self,filter_id):
        result=None
        try:
            result=super(IssueFilterManager,self).get_queryset().get(id=filter_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    def project_issue_filter(self,project_id):
        result=None
        try:
            result=self.all().filter(Project=project_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def user_issue_filter(self,user_id):
        result=None
        try:
            result=self.all().filter(Creator=user_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    
    
    
    
            



        
    
        
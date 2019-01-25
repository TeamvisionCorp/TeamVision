#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from model_managers.model_manager import ModelManager



class WebappManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(WebappManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,app_id):
        result=None
        try:
            result=super(WebappManager,self).get_queryset().get(id=app_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
class TaskQueueManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(TaskQueueManager,self).get_queryset()
    
    def get(self,queue_id):
        result=None
        try:
            result=super(TaskQueueManager,self).get_queryset().get(id=queue_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_agent_tasks(self,agent_id):
        return self.all().filter(AgentID=agent_id).filter(Command=1).filter(Status__gt=3).exclude(Status=10)

class AgentManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(AgentManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,agent_id):
        result=None
        try:
            result=super(AgentManager,self).get_queryset().get(id=agent_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_by_ip(self,agent_ip):
        result=None
        try:
            result=super(AgentManager,self).get_queryset().get(IP=agent_ip)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result



class TeamManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):

        return super(TeamManager,self).get_queryset().filter(IsActive=1)

    def get(self,team_id):
        result=None
        try:
            result=super(TeamManager,self).get_queryset().get(id=team_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result



class FileManager(ModelManager):
    '''
    classdocs
    '''
    def all(self,is_active=True):
        if is_active:
            return super(FileManager,self).get_queryset().filter(IsActive=1)
        else:
            return super(FileManager,self).get_queryset()
            
    
    def get(self,file_id):
        result=None
        try:
            result=super(FileManager,self).get_queryset().get(id=file_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class ErrorMessageManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(ErrorMessageManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,error_code):
        result=None
        try:
            result=self.all().filter(ErrorCode=error_code)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class DicDataManager(ModelManager):
    
    def all(self):
        
        return super(DicDataManager,self).get_queryset().filter(DicDataIsActive=1)
    
    def get(self,dicdata_id):
        result=None
        try:
            result=super(DicDataManager,self).get_queryset().get(id=dicdata_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_datas_bytype(self,type_id):
        return self.all().filter(DicType_id=type_id)
    
    def get_data_byvalue(self,value,type_id):
        result=None
        all_data=self.all().filter(DicType_id=type_id)
        for data in all_data:
            if data.DicDataValue==value:
                result=data
                break
        return result;

class DicTypeManager(ModelManager):
    
    def all(self):
        
        return super(DicTypeManager,self).get_queryset().filter(DicTypeIsActive=1)
    
    def get(self,dictype_id):
        result=None
        try:
            result=super(DicTypeManager,self).get_queryset().get(id=dictype_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def get_by_name(self,type_name):
        result=None
        try:
            result=super(DicTypeManager,self).get_queryset().get(DicTypeName=type_name)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result    

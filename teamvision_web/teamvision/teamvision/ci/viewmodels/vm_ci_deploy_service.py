#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.models import CIDeployService
from teamvision.home.models import FileInfo
from business.ci.ci_service import CIService

class VM_CIDeployService(object):
    '''
    classdocs
    '''


    def __init__(self,dm_deploy_service,selected_service_id):
        '''
        Constructor
        '''
        self.ci_service=dm_deploy_service
        self.selected_service_id=selected_service_id
    
    
    def is_selected(self):
        result=""
        if self.ci_service.id==self.selected_service_id:
            result="selected"
        return result
    
    def get_uploaded_files(self):
        result=list()
        if self.ci_service.RelatedFiles:
            file_ids=eval(self.ci_service.RelatedFiles)
            for file_id in file_ids:
                temp_file=FileInfo.objects.get(int(file_id))
                result.append(temp_file)
        return result
    
    def is_avaliable(self):
        result=False
        if self.ci_service.Project!=0:
            result=True
        if self.ci_service.DeployDir!="":
            result=True
        return result
    
    def get_replace_config(self):
        result=None
        if self.ci_service.AdvanceConfig:
            result=CIService.get_replace_config(self.ci_service.AdvanceConfig)
            for file in result.replace_target_map:
                print(file.file_name)
        return result
                 
            
        
   
    
    
    
                
        
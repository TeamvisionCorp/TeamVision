#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.models import CIDeployService
from teamvision.home.models import FileInfo
from business.ci.ci_service import CIService

class VM_CIServiceRPFile(object):
    '''
    classdocs
    '''


    def __init__(self,service_file,selected_files):
        '''
        Constructor
        '''
        self.service_file=service_file
        self.selected_files=selected_files
    
    
    def is_checked(self):
        result=""
        if self.selected_files:
            if str(self.service_file.file_id) in self.selected_files:
                result="checked"
        return result
                 
            
        
   
    
    
    
                
        
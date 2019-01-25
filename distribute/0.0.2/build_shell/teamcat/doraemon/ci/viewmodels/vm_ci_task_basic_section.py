#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''


from business.ci.ci_task_config_service import CITaskConfigService
from doraemon.ci.models import BasicSection,SCMSection,PreBuildSection,PostBuildSection,BuildSection

class VM_BasicSection(object):
    '''
    classdocs
    '''


    def __init__(self,basic_section):
        '''
        Constructor
        '''
        self.basic_section=basic_section
    
    def get_asgin_agent(self):
        result=0
        if self.get_parameter_value("ci_agent_select"):
            result=int(self.get_parameter_value("ci_agent_select"))
        return result
    
    
    def get_agent_filter_condations(self):
        result=""
        if self.basic_section['plugins']:
            result=self.get_parameter_value("agent_condations")
        return result
    
    def get_schedule_rule(self):
        return self.get_parameter_value("time_trigger")
    
    def get_case_filters(self):
        result=""
        if self.basic_section['plugins']:
            result=self.get_parameter_value("autocase_filter")
        return result
 
    def is_agent_asgin(self):
        result=""
        if self.get_parameter_value("agent_filter_type")=='1':
            result="checked"
        return result
    
    def is_agent_filter(self):
        result=""
        if self.get_parameter_value("agent_filter_type")!='1':
            result="checked"
        return result
    
    def is_time_trigger(self):
        result=""
        if self.get_parameter_value("ci_task_trigger"):
            result="checked"
        return result
    
    def get_parameter_value(self,parameter_name):
        result=""
        if self.basic_section['plugins']:
            for parameter in self.basic_section['plugins'][0]['parameter']:
                if parameter.get('name')==parameter_name:
                    result=parameter.get('value')
        return result
        
        
    
    
   
    
    
    
                
        
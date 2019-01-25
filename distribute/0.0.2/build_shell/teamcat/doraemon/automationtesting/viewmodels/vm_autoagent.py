#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from dataaccess.common.dal_dictvalue import DAL_DictValue

class VM_AutoAgent(object):
    '''
    AutomationTask business model
    '''
    
    def __init__(self,autoagent):
        ''' dm_automationtask wapper
        '''
        self.autoagent=autoagent
    
    def get_autoagent_name(self):
        return self.autoagent.AName
    
    def get_os(self):
        agent_os="--"
        if self.autoagent.AOS!=0:
            agent_os=DAL_DictValue.get_dataname_by_datavalue("AgentOSType",self.autoagent.AOS).DicDataName
        return agent_os
    
    
    def get_ip(self):
        agent_ip="--"
        if self.autoagent.AIP!="":
            agent_ip=self.autoagent.AIP
        return agent_ip
    

            
    def get_browsers(self):
        browsers="--"
        if self.autoagent.AAgentBrowser!="":
            browsers=""
            browsers_list=eval(self.autoagent.AAgentBrowser)
            print(browsers_list)
            for browserid in browsers_list:
                browsers=browsers+DAL_DictValue.get_dataname_by_datavalue("AutoTaskRuntime",browserid).DicDataName+" "
#             browsers=browsers[0,len(browsers)]
        return browsers
    
    
    
    
    def get_status(self):
        return DAL_DictValue.get_dataname_by_datavalue("AutoAgentStatus",self.autoagent.AStatus).DicDataName
    
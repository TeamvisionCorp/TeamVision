#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from dataaccess.common.dal_dictvalue import DAL_DictValue
from dataaccess.automationtesting.dal_autoagent import DAL_AutoAgent

class VM_AutoMobileDevice(object):
    '''
    auto mobile device business model
    '''
    
    def __init__(self,automobiledevice):
        ''' dm_automationtask wapper
        '''
        self.automobiledevice=automobiledevice
    
    def get_automobiledevice_name(self):
        return self.automobiledevice.MDeviceName
    
    def get_os(self):
        return self.automobiledevice.MDeviceOS+":"+self.automobiledevice.MDOSVersion
    
    
    def get_screen(self):
        agent_ip="--"
        return self.automobiledevice.MDeviceScreen
    

            
    def get_hostmachine(self):
        machine_name="--"
        if self.automobiledevice.MDeviceAgent:
            agent=DAL_AutoAgent.get_autoagent(id)
            machine_name=agent.AName
        return machine_name
    
    
    
    
    def get_status(self):
        return "--"
#         return DAL_DictValue.get_dataname_by_datavalue("AutoAgentStatus",self.automobiledevice.AStatus).DicDataName
    
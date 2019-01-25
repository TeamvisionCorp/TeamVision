#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from dataaccess.common.dal_dictvalue import DAL_DictValue

class VM_AutoRunResult(object):
    '''
    auto mobile device business model
    '''
    
    def __init__(self,autorunresult):
        ''' dm_automationtask wapper
        '''
        self.autorunresult=autorunresult
    
    def get_autorunresult_total(self):
        
        return self.autorunresult.TRTotal
    
    def get_autorunresult_pass(self):
        return self.autorunresult.TRPass
    
    def get_autorunresult_fail(self):
        return self.autorunresult.TRFail
    
    def get_autorunresult_aborted(self):
        return self.autorunresult.TRAborted
    
    def get_starttime(self):
        return self.autorunresult.TRStartTime
    
    
    def get_endtime(self):
        return self.autorunresult.TREndTime
    
    
    def get_status(self):
        return "OK"
#         return DAL_DictValue.get_dataname_by_datavalue("AutoAgentStatus",self.autorunresult.AStatus).DicDataName
    
#coding=utf-8
'''
Created on 2017年4月20日

@author: ethan
'''

class VM_Logger(object):
    '''
    logger view modle
    '''


    def __init__(self,dm_logger):
        '''
        
        '''
        self.logger=dm_logger
    
    
    @property
    def app_name(self):
        result=""
        app_id=self.logger.appId
        if app_id==1:
            result="识字"
        if app_id==2:
            result="故事"
        if app_id==3:
            result="数学"
        if app_id==4:
            result="词典"
        if app_id==5:
            result="背单词"   
        if app_id==6:
            result="英语"
        return result
        
        
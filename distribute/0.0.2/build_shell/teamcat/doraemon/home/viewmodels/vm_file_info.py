#coding=utf-8
'''
Created on 2015-11-27

@author: zhangtiande
'''

from doraemon.home.models import FileInfo
from gatesidelib.common.simplelogger import SimpleLogger

class VM_FileInfo(object):
    '''
    classdocs
    '''


    def __init__(self,file_info):
        '''
        Constructor
        '''
        self.file=file_info
        
    
    def file_size(self):
        result="0 K"
        try:
            if int(self.file.FileSize/1024)==0:
                result=str(self.file.FileSize)+" K"
            else:
                result=str(int(self.file.FileSize/1024))+"M"
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result;
            
        
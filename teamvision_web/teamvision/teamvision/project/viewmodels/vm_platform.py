#coding=utf-8
'''
Created on 2015-12-15

@author: Devuser
'''

class VM_Platform(object):
    '''
    classdocs
    '''


    def __init__(self,platform,selectd_platform):
        '''
        Constructor
        '''
        self.platform=platform
        self.selectd_platform=selectd_platform
    
    def is_selected(self):
        result=""
        if self.platform.DicDataValue==self.selectd_platform:
            result="selected"
        return result
#coding=utf-8
'''
Created on 2015-1-7

@author: Devuser
'''
import os,platform

class CommonHelper(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_slash():
        if os.name=='nt':
            return "\\"
        else:
            return "/"
        
    @staticmethod
    def is_windows():
        result=True
        if not 'Windows' in platform.system():
            result=False
        return result
            
            
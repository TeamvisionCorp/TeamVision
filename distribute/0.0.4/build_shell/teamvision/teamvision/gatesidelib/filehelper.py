#coding=utf-8
#coding=utf-8

'''
Created on 2014-12-10

@author: Devuser
'''

from gatesidelib.common.simplelogger import SimpleLogger
import os
import stat
import shutil

class FileHelper(object):
    
    @staticmethod
    def write_lines(filename,linelist):
        filehandler=open(filename,'w')
        filehandler.writelines(linelist)
        filehandler.close()
    
    @staticmethod
    def read_lines(filename):
        filehandler=open(filename,'r')
        result=filehandler.readlines()
        filehandler.close()
        return result
    
    @staticmethod
    def get_linecounts(filename):
        count=0
        filehandler=open(filename,'rb')
        while True:
            buffer=filehandler.read(1024*8192)
            if not buffer:
                break
            count +=buffer.count('\n')
        filehandler.close()
        return count
    
    @staticmethod
    def delete_file(filename):
        if os.path.isfile(filename):
            os.remove(filename)
    @staticmethod
    def delete_dir_all(dirpath):
        try:
            shutil.rmtree(dirpath) 
        except Exception as ex:
            SimpleLogger.error(ex)
            
    @staticmethod
    def delete_empty_dir(dirpath):
        if os.path.exists(dirpath):
            os.rmdir(dirpath)
        

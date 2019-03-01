#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''


from gatesidelib.common.simplelogger import SimpleLogger


class VM_CIHistoryChangeFile(object):
    '''
    classdocs
    '''
    
    def __init__(self,file_changes):
        self.file_changes=file_changes
        self.new_path=self.get_property("newPath")
        self.old_path=self.get_property("oldPath")
        self.change_type=self.get_property("type")
    
    def file_change_type_icon(self):
        result=""
        if self.change_type.upper()=="A":
            result="fa-plus status-success"
        if self.change_type.upper()=="M":
            result="fa-pencil-square-o status-default"
        
        if self.change_type.upper()=="D status-fail":
            result="fa-minus"
        
        if self.change_type.upper()=="C status-success":
            result="fa-copy"
        
        if self.change_type.upper()=="C status-success":
            result="fa-plus"
        return result
    
        
    def get_property(self,property_name):
        result=""
        try:
            result=self.file_changes[property_name]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
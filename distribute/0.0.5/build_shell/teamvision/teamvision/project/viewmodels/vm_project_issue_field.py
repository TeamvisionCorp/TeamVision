#coding=utf-8
'''
Created on 2014-2-16

@author: zhangtiande
'''

class VM_IssueField(object):
    '''
    MyPlace business model
    '''
    
    def __init__(self,issue_field,selected_value):
        self.issue_field=issue_field
        self.selected_value=selected_value
    
    
    def is_selected_style(self):
        if self.issue_field.Value==self.selected_value:
            return "fa-check"
        else:
            return ""
        
    def is_selected(self):
        if self.issue_field.Value==self.selected_value:
            return "selected"
        else:
            return ""
    
    
    
    def is_checked(self):
        result=""
        if isinstance(self.selected_value,list):
            if self.issue_field.Value in self.selected_value:
                result="checked"
        else:
            if self.issue_field.Value==self.selected_value:
                result="checked"
        return result
            
            
        
            
        
        
            
        
        
        
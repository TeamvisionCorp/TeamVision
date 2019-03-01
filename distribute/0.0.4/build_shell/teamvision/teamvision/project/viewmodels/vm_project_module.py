#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: zhangtiande
'''

class VM_ProjectModule(object):
    '''
    MyPlace business model
    '''
    
    def __init__(self,module,selected_module):
        self.module=module
        self.selected_module=selected_module
    
    
    def is_selected(self):
        if self.module.id==self.selected_module:
            return "selected"
        else:
            return ""
        
    def is_selected_style(self):
        if self.module.id==self.selected_module:
            return "fa-check"
        else:
            return ""
            
            
        
            
        
        
            
        
        
        
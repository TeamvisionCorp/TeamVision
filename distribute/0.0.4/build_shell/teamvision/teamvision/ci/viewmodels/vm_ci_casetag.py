#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

class VM_CICaseTag(object):
    '''
    classdocs
    '''


    def __init__(self,dm_case_tag,selected_value):
        '''
        Constructor
        '''
        self.ci_tag=dm_case_tag
        self.selected_tags=selected_value
        

    def is_selected(self):
        result=""
        if self.selected_tags:
            if self.ci_tag.id in eval(self.selected_tags):
                result="selected"
        return result
        
        
        
                 
            
        
   
    
    
    
                
        
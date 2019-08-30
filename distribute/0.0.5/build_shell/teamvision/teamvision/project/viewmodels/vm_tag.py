#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''
 

class VM_Tag(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_tag,select_tag_ids):
        self.tag=dm_tag
        self.select_tags=select_tag_ids
    
    def is_checked(self):
        if self.select_tags:
            if self.tag.id in eval(self.select_tags):
                return "fa-check"
            else:
                return ""
    
    def is_selectd(self):
        if self.select_tags:
            if self.tag.id in eval(self.select_tags):
                return "selected"
            else:
                return ""
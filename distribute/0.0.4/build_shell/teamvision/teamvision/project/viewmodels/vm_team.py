#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: zhangtiande
'''

class VM_Team(object):
    '''
    MyPlace business model
    '''
    
    def __init__(self,team,selected_team):
        self.team=team
        self.selected_team=selected_team




    def is_selected(self):
        if self.team.id==self.selected_team:
            return "selected"
        else:
            return ""
        
    def is_selected_style(self):
        if self.team.id==self.selected_team:
            return "fa-check"
        else:
            return ""
            
            
        
            
        
        
            
        
        
        
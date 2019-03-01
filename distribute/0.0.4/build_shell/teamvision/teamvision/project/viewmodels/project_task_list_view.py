#coding=utf-8
'''
Created on 2015-10-10

@author: Devuser
'''


class ProjectTaskList(object):
    
    def __init__(self,fullpart,tasks,tag_menu,owner_menu,show_user=True,show_tag=True):
        self.fullpart=fullpart
        self.tasks=tasks
        self.showuser=show_user
        self.show_tag=show_tag
    


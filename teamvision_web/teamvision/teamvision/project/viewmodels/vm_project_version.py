#coding=utf-8
'''
Created on 2015-11-9

@author: Devuser
'''

from teamvision.project.models import Project
from teamvision.project.viewmodels.vm_project import VM_Project

class VM_ProjectVersion(object):
    



    def __init__(self,version,selected_version=0):
        '''
        Constructor
        '''
        self.version=version
        self.selected_versions=selected_version
    
    
    def platform(self):
        return "fa-android"
    
    
    def project_title(self):
        dm_project=Project.objects.get(self.version.VProjectID)
        vm_project=VM_Project(0,False,dm_project,self.version.VProjectID)
        return vm_project.platform_title()+"_"+dm_project.PBTitle
    
    def is_selected(self):
        if self.version.id==self.selected_versions:
            return "fa-check"
        else:
            return ""
    
    def dropdown_selected(self):
        result=""
        if isinstance(self.selected_versions,list):
            if self.version.id in self.selected_versions:
                result="selected"
        else:
            if self.version.id==self.selected_versions:
                result="selected"
        return result
#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''

from doraemon.project.models import Version
from doraemon.home.models import FileInfo
from doraemon.home.viewmodels.vm_file_info import VM_FileInfo
 

class VM_Archive(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_archive):
        self.archive=dm_archive
        
    
    def version(self):
        version=Version.objects.get(self.archive.VersionID)
        return version
    
    def file_infos(self):
        result=list()
        for file_id in eval(self.archive.Archives):
            file_info=FileInfo.objects.get(int(file_id))
            temp=VM_FileInfo(file_info)
            result.append(temp)
        return result
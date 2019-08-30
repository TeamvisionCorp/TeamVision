#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from teamvision.project.models import Project,Version,ProjectMember,\
    ProjectArchive
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from teamvision.home.models import FileInfo

class ArchiveService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_project_archive_versions(project_id):
        result=list()
        all_project_archives=ProjectArchive.objects.get_project_archives(project_id)
        for archive in all_project_archives:
            if archive.VersionID not in result:
                result.append(archive.VersionID)
        return result
    
    @staticmethod
    def get_project_version_files(version_id):
        all_version_archives=ProjectArchive.objects.get_version_archives(version_id)
        return all_version_archives
    
    @staticmethod
    def log_create_activity(user,target):
        Version.objects.log_action(user.id,target.id,target.VVersion,ADDITION,"创建了新版本",target.VProjectID)
    
    @staticmethod
    def log_delete_activity(user,target):
        Version.objects.log_action(user.id,target.id,target.VVersion,ADDITION,"删除了版本",target.VProjectID)
    
    @staticmethod
    def log_change_activity(user,target):
        Version.objects.log_action(user.id,target.id,target.VVersion,ADDITION,"修改了版本",target.VProjectID)
        
        
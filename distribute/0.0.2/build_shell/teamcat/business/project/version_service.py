#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from doraemon.project.models import Project,Version,ProjectMember
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION

class VersionService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_latests_project_ids(request):
        result=list()
        my_project_ids=[member.PMProjectID for member in ProjectMember.objects.all().filter(PMMember=request.user.id)]
        project_versions=Version.objects.all().filter(VProjectID__in=my_project_ids).order_by("-id")
        for version in project_versions:
            if version.VProjectID not in result:
                result.append(version.VProjectID)
        for project_id in my_project_ids:
            if project_id not in result:                  
                result.append(project_id)
        return result
    
    @staticmethod
    def get_latest_version(project_id):
        result=None
        try:
            project_versions=Version.objects.all().filter(VProjectID=project_id).order_by("-id")
            if project_versions:
                result=project_versions[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    @staticmethod
    def get_project_version(project_id):
        result=None
        try:
            project_versions=Version.objects.all().filter(VProjectID=int(project_id)).order_by("-id")
            result=project_versions
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    @staticmethod
    def get_version(version_id):
        return Version.objects.get(version_id)
        
    
    
        
        


    @staticmethod
    def create_version(request,projectid):
        try:
            version=Version()
            version.VProjectID=projectid
            version.VVersion=request.POST.get('VVersion')
            version.CFTCommitor=request.user.id
            version.save()
            VersionService.log_create_activity(request.user, version)
        except Exception as ex:
            SimpleLogger.exception(ex)
            
    
    
    @staticmethod
    def edit_version(request,version_id):
        version=Version.objects.get(version_id)
        version=VersionService.init_fortesting(request,version)
        version.save()
        VersionService.log_change_activity(request.user, version)
    
    
    @staticmethod
    def delete_version(request,version_id):
        version=Version.objects.get(version_id)
        version.IsActive=0
        version.save()
        VersionService.log_delete_activity(request.user, version)
    
    
    @staticmethod
    def update_version(request,version_id):
        version=Version.objects.get(version_id)
        version.VVersion=request.POST.get("VVersion")
        version.save()
        VersionService.log_change_activity(request.user, version)
    
    
    @staticmethod
    def update_date(request,version_id):
        version=Version.objects.get(version_id)
        start_date=request.POST.get("VStartDate")
        release_date=request.POST.get("VReleaseDate")
        if start_date:
            version.VStartDate=start_date
        if release_date:
            version.VReleaseDate=release_date
        version.save()
        VersionService.log_change_activity(request.user, version)
            
        
    
    
    @staticmethod
    def log_create_activity(user,target):
        Version.objects.log_action(user.id,target.id,target.VVersion,ADDITION,"创建了新版本",target.VProjectID)
    
    @staticmethod
    def log_delete_activity(user,target):
        Version.objects.log_action(user.id,target.id,target.VVersion,ADDITION,"删除了版本",target.VProjectID)
    
    @staticmethod
    def log_change_activity(user,target):
        Version.objects.log_action(user.id,target.id,target.VVersion,ADDITION,"修改了版本",target.VProjectID)
        
        
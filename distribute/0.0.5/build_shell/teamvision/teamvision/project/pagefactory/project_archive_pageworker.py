#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.project.pagefactory.project_pageworker import ProjectPageWorker
from teamvision.project.viewmodels.project_left_nav_bar import ProjectArchiveLeftNavBar
from teamvision.project.pagefactory.project_template_path import ProjectArchivePath
from business.project.archive_service import ArchiveService
from teamvision.project.models import Version
from teamvision.home.viewmodels.vm_file_info import VM_FileInfo
from teamvision.ci.viewmodels.vm_ci_build_file import VM_CIBuildFile
from teamvision.home.models import FileInfo


class ProjectArchivePageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.left_nav_bar_model=ProjectArchiveLeftNavBar
    
    def get_index_page(self,request,projectid,version):
        left_nav_bar=self.get_archive_left_bar(request,projectid,sub_nav_action="all")
        pagefileds={'left_nav_bar':left_nav_bar,'web_app_view':self.get_web_app(projectid,version)}
        return self.get_full_page_with_header(request, pagefileds, projectid,ProjectArchivePath.archive_index_page_path)
    
    def get_web_app(self,projectid,version):
        project_archive_folder_list=self.get_archive_item(projectid,version)
        pagefileds={'project_archive_folder_list':project_archive_folder_list,'project_id':projectid}
        return self.get_webpart(pagefileds,ProjectArchivePath.archive_webapp)
    
    def get_archive_item(self,project_id,version_id):
        item_list=list()
        folder=True
        if version_id!="all":
            folder=False
            item_list=self.get_archive_version_files(version_id)
        else:
            item_list=self.get_archive_versions(project_id)  
        pagefileds={'item_list':item_list,"folder":folder}
        return self.get_webpart(pagefileds,ProjectArchivePath.archive_item)
    
    
    def get_archive_versions(self,project_id):
        result=list()
        version_ids=ArchiveService.get_project_archive_versions(project_id)
        for versionid in version_ids:
            temp_version=Version.objects.get(versionid)
            result.append(temp_version)
        return result 
    
    def get_archive_version_files(self,version_id):
        result=list()
        version_archives=ArchiveService.get_project_version_files(version_id)
        for archive in version_archives:
            for fileid in eval(archive.Archives):
                if fileid!="":
                    file_info=FileInfo.objects.get(int(fileid))
                    temp_file=VM_FileInfo(file_info)
                    result.append(temp_file)
        return result 
    
    
    
    def get_archive_left_bar(self,request,projectid, sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,projectid,ProjectArchivePath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    
   
        
    
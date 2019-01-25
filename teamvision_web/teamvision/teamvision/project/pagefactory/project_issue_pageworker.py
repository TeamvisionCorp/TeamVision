#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.project.pagefactory.project_pageworker import ProjectPageWorker
from teamvision.project.viewmodels.project_left_nav_bar import ProjectIssueLeftNavBar
from teamvision.project.pagefactory.project_template_path import ProjectIssuePath
from teamvision.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from business.project.memeber_service import MemberService
from teamvision.project.models import ProjectIssue,IssueFilter
from teamvision.project import models
from teamvision.project.mongo_models import IssueMongoFile
from teamvision.project.viewmodels.vm_project_issue import VM_ProjectIssue
from teamvision.project.viewmodels.vm_project_member import VM_ProjectMember
from teamvision.project.viewmodels.vm_project_issue_field import VM_IssueField
from business.project.issue_service import IssueService
from business.common.redis_service import RedisService
from teamvision.project.viewmodels.vm_issue_activity import VM_IssueActivity
from teamvision.project.viewmodels.vm_project_issue_filter import VM_IssueFilter
import filetype
from teamvision.home.models import FileInfo
from business.common.file_info_service import FileInfoService


class ProjectIssuePageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.left_nav_bar_model=ProjectIssueLeftNavBar
    
    def get_index_page(self,request,projectid,issue_id):
        left_nav_bar=self.get_issue_left_bar(request,projectid,sub_nav_action="all")
        pagefileds={'left_nav_bar':left_nav_bar,'web_app_view':self.get_web_app(projectid,issue_id),'issue_id':issue_id}
        return self.get_full_page_with_header(request, pagefileds, projectid,ProjectIssuePath.issue_index_page_path)
    
    def get_web_app(self,project_id,version):
        issue_filter=self.get_issue_filter(project_id)
        issue_item=self.get_issue_item(project_id,0)
        pagefileds={'issue_filter':issue_filter,'issue_item':issue_item,'project_id':project_id}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_webapp)
    
    def get_issue_create_dialog(self,request,projectid):
        dm_issue=ProjectIssue()
        vm_issue=VM_ProjectIssue(request.user.id,dm_issue)
        form_html=self.get_issue_form_controll(request,projectid,vm_issue)
        pagefileds={'formhtml':form_html}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_create_dialog_path)
    
    def get_issue_form_controll(self,request,projectid,vm_issue):
        project_dorpdownlist=ProjectCommonControllPageWorker.get_myproject_dropdown_list(self, request, 0)
        module_dorpdownlist=ProjectCommonControllPageWorker.get_module_dropdown_list(self, projectid,0)
        version_dorpdownlist=ProjectCommonControllPageWorker.get_version_dropdown_list(self,projectid,0,False)
        issue_category=ProjectCommonControllPageWorker.get_issue_field_dropdown_list(self,models.ProjectIssueCategory,0)
        issue_severity=ProjectCommonControllPageWorker.get_issue_field_dropdown_list(self,models.ProjectIssueSeverity,0)
        member_users=MemberService.get_member_users(projectid)
        project_members=ProjectCommonControllPageWorker.get_member_dropdownlist(self, member_users, projectid,request.user.id)
        project_phase=ProjectCommonControllPageWorker.get_issue_field_dropdown_list(self,models.ProjectPhase,0)
        os_dropdown_list=ProjectCommonControllPageWorker.get_issue_field_dropdown_list(self,models.ProjectOS,0)
        os_version_dropdown_list=ProjectCommonControllPageWorker.get_os_version_dropdown_list(self,models.ProjectOSVersion,1,0)
        team_dropdown_list=ProjectCommonControllPageWorker.get_team_dropdown_list(self,0)
        pagefileds={'issue':vm_issue,"module_dorpdownlist":module_dorpdownlist,"project_dorpdownlist":project_dorpdownlist}
        pagefileds['version_dorpdownlist']=version_dorpdownlist
        pagefileds["issue_category"]=issue_category
        pagefileds["issue_severity"]=issue_severity
        pagefileds["project_phase"]=project_phase
        pagefileds["project_members"]=project_members
        pagefileds["os_dropdown_list"]=os_dropdown_list
        pagefileds["os_version_dropdown_list"]=os_version_dropdown_list
        pagefileds["team_dropdown_list"]=team_dropdown_list
        return self.get_webpart(pagefileds, ProjectIssuePath.issue_create_form_path)

        
    
    
    
    
    def get_issue_detail(self,issue_id):
        dm_issue=ProjectIssue.objects.get(issue_id)
        vm_issue=VM_ProjectIssue(self.request.user.id,dm_issue)
        status_dropdown_menu=ProjectCommonControllPageWorker.get_issue_field_dropdown_menu(self,models.ProjectIssueStatus,dm_issue.Status)
        solution_dropdown_menu=ProjectCommonControllPageWorker.get_issue_field_dropdown_menu(self,models.ProjectIssueResolvedResult,dm_issue.Solution)
        severity_dropdown_menu=ProjectCommonControllPageWorker.get_issue_field_dropdown_menu(self,models.ProjectIssueSeverity,dm_issue.Severity)
        category_dropdown_menu=ProjectCommonControllPageWorker.get_issue_field_dropdown_menu(self,models.ProjectIssueCategory,dm_issue.IssueCategory)
        phase_dropdown_menu=ProjectCommonControllPageWorker.get_issue_field_dropdown_menu(self,models.ProjectPhase,dm_issue.ProjectPhase)
        os_dropdown_menu=ProjectCommonControllPageWorker.get_issue_field_dropdown_menu(self,models.ProjectOS,dm_issue.DeviceOS)
        os_version_dropdown_menu=ProjectCommonControllPageWorker.get_issue_device_version_dropdown_menu(self,dm_issue.DeviceOS,dm_issue.OSVersion)
        member_users=MemberService.get_member_users(dm_issue.Project)
        member_dropdown_menu=ProjectCommonControllPageWorker.get_member_dropdown_menu(self, member_users, dm_issue.Project, dm_issue.Processor)
        module_dropdown_menu=ProjectCommonControllPageWorker.get_module_dropdown_menu(self,dm_issue.Project, dm_issue.Module)
        version_dropdown_menu=ProjectCommonControllPageWorker.get_version_dropdown_menu(self,dm_issue.Project, dm_issue.Version)
        issue_attachment_upload_dropdown_menu=ProjectCommonControllPageWorker.get_issue_upload_dropdown_menu(self)
        issue_detail_activity=self.get_issue_detail_activity(issue_id)
        team_dropdown_menu=ProjectCommonControllPageWorker.get_team_dropdown_menu(self,dm_issue.Team)
        pagefileds={"issue":vm_issue,"status_dropdown_menu":status_dropdown_menu} 
        pagefileds['member_dropdown_menu']=member_dropdown_menu
        pagefileds['module_dropdown_menu']=module_dropdown_menu
        pagefileds['version_dropdown_menu']=version_dropdown_menu
        pagefileds['solution_dropdown_menu']=solution_dropdown_menu
        pagefileds['severity_dropdown_menu']=severity_dropdown_menu
        pagefileds['category_dropdown_menu']=category_dropdown_menu
        pagefileds['phase_dropdown_menu']=phase_dropdown_menu
        pagefileds['os_dropdown_menu']=os_dropdown_menu
        pagefileds['os_version_dropdown_menu']=os_version_dropdown_menu
        pagefileds['issue_attachment_upload_dropdown_menu']=issue_attachment_upload_dropdown_menu
        pagefileds['issue_detail_activity']=issue_detail_activity
        pagefileds['team_dropdown_menu']=team_dropdown_menu
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_detail)
    
    def get_issue_context(self,project_id):
        dm_members=MemberService.get_member_users(project_id)
        members=list()
        for dm_member in dm_members:
            temp_vm_member=VM_ProjectMember(project_id,dm_member,None,None)
            members.append(temp_vm_member)
        pagefileds={"members":members} 
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_context_menu)
    
    def get_issue_detail_activity(self,issue_id):
        dm_activities=models.IssueActivity.objects.issue_activity(issue_id)
        vm_activities=list()
        for activity in dm_activities:
            temp=VM_IssueActivity(activity)
            vm_activities.append(temp)
        pagefileds={"activities":vm_activities}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_detail_activity)
    
    def get_issue_filter(self,project_id):
        issue_filter_body=self.get_issue_filter_body(project_id,0)
        filter_menu_list=self.get_issue_filter_menu(self.request.user.id)
        pagefileds={"issue_filter_body":issue_filter_body}
        pagefileds['filter_menu_list']=filter_menu_list
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_filter) 
    
    
    def get_issue_filter_body(self,projectid,filter_id=0):
        if str(filter_id)!="0":
            issue_filter=IssueFilter.objects.get(int(filter_id))
            vm_issue_filter=VM_IssueFilter(issue_filter,projectid)
        else:
            vm_issue_filter=VM_IssueFilter(None,projectid)    
        project_dropdown_list=ProjectCommonControllPageWorker.get_myproject_dropdown_list(self, self.request,vm_issue_filter.project())
        member_users=MemberService.get_member_users(vm_issue_filter.project())
        processor_dropdown_list=ProjectCommonControllPageWorker.get_member_dropdownlist(self, member_users, vm_issue_filter.project(),vm_issue_filter.processors())
        reporter_dropdown_list=ProjectCommonControllPageWorker.get_member_dropdownlist(self, member_users, vm_issue_filter.project(),vm_issue_filter.creators())
        project_version_dropdown_list=ProjectCommonControllPageWorker.get_version_dropdown_list(self,vm_issue_filter.project(),vm_issue_filter.versions(),True)
        team_dropdown_list=ProjectCommonControllPageWorker.get_team_dropdown_list(self,0)
        pagefileds={"processor_dropdown_list":processor_dropdown_list}
        pagefileds['reporter_dropdown_list']=reporter_dropdown_list
        pagefileds['project_dropdown_list']=project_dropdown_list
        pagefileds['status_list']=self.get_issue_field_list(models.ProjectIssueStatus.objects.all(),vm_issue_filter.status())
        pagefileds['severity_list']=self.get_issue_field_list(models.ProjectIssueSeverity.objects.all(),vm_issue_filter.severity())
        pagefileds['solution_list']=self.get_issue_field_list(models.ProjectIssueResolvedResult.objects.all(),vm_issue_filter.solution())
        pagefileds['project_version_dropdown_list']=project_version_dropdown_list
        pagefileds['create_date']=vm_issue_filter.create_date
        pagefileds['team_dropdown_list']=team_dropdown_list
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_filter_body)
    
    def get_issue_field_list(self,dm_fields,selected_value):
        result=list()
        for item in dm_fields:
            temp=VM_IssueField(item,selected_value)
            result.append(temp)
        return result
    
    def get_issue_item(self,project_id,user_id):
        issue_context=self.get_issue_context(project_id)
        issue_list_controll=self.get_issue_more(project_id, user_id,0)
        issue_count=len(IssueService.all_issues(project_id,user_id))
        key=str(user_id)+"_issue_searchkeyword"
        search_word=RedisService.get_value(key)
        pagefileds={"issue_context":issue_context,"issue_list_controll":issue_list_controll,"issue_count":issue_count,"search_word":search_word}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_item_list)
    
    def get_issue_more(self,project_id,user_id,page_index):
        start_issue_index=int(page_index*10)
        end_issue_index=int((page_index+1)*10)
        dm_issues=IssueService.all_issues(project_id,user_id)[start_issue_index:end_issue_index]
        issue_items=list()
        for dm_issue in dm_issues:
            temp_vm_issue=VM_ProjectIssue(self.request.user.id,dm_issue)
            issue_items.append(temp_vm_issue)
        pagefileds={"issue_items":issue_items}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_item_controll)
    
    
    
    def get_my_issue_item(self,user_id,user_role):
        issue_list_controll=self.get_my_issue_more(user_id,0,user_role)
        issue_count=len(IssueService.my_issue(user_id,user_role))
        key=str(user_id)+"_issue_searchkeyword"
        search_word=RedisService.get_value(key)
        pagefileds={"issue_list_controll":issue_list_controll,"issue_count":issue_count,"search_word":search_word}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_item_list)
    
    def get_my_issue_more(self,user_id,page_index,user_role):
        start_issue_index=int(page_index*10)
        end_issue_index=int((page_index+1)*10)
        dm_issues=IssueService.my_issue(user_id,user_role)[start_issue_index:end_issue_index]
        issue_items=list()
        for dm_issue in dm_issues:
            temp_vm_issue=VM_ProjectIssue(self.request.user.id,dm_issue)
            issue_items.append(temp_vm_issue)
        pagefileds={"issue_items":issue_items}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_item_controll)
    
    def get_issue_upload_dialog(self,request,issue_id):
        pagefileds={'issue_id':issue_id}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_upload_attachments_dialog)
    
    def get_issue_operation_dialog(self,request,issue_id,operation_type):
        solution_dorpdownlist=ProjectCommonControllPageWorker.get_issue_field_dropdown_list(self,models.ProjectIssueResolvedResult,0)
        pagefileds={"solution_dorpdownlist":solution_dorpdownlist,'issue_id':issue_id,"operation_type":operation_type}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_operation_dialog)
    
    def get_issue_filter_save_dialog(self,request,filter_id):
        filter_name=""
        if str(filter_id)!="0":
            filter_name=models.IssueFilter.objects.get(int(filter_id)).FilterName
        pagefileds={'filter_id':filter_id,'filter_name':filter_name}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_filter_save_dialog)
    
    
    def get_issue_attachment_viewer(self,issue_id,attachment_id):
        temp_file=FileInfoService.get_file(int(attachment_id),IssueMongoFile).read()
        kind = filetype.guess(temp_file)
        file_type=0
        file_content=""
        if kind:
            if kind.mime.startswith("image"):
                file_type=1
            if kind.mime.startswith("video"):
                file_type=2
        pagefileds={'file_id':attachment_id,'file_type':file_type,'issue_id':issue_id}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_attachment_viewer)
    
    def get_issue_attachment_view_iframe(self,attachment_id):
        pagefileds={'file_id':attachment_id}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_attachment_viewe_iframe)
    
    def get_issue_filter_menu(self,user_id):
        filters=IssueFilter.objects.user_issue_filter(int(user_id))
        pagefileds={'filters':filters}
        return self.get_webpart(pagefileds,ProjectIssuePath.issue_filter_menu_items)
    
    def get_filter_field(self,key):
        issue_filter_cache=IssueService.filter_value_dict(str(self.request.user.id)+"_issue_filter")
        result=0
        if issue_filter_cache.get(key):
            result=issue_filter_cache[key]
        return result
            

            
    def get_issue_left_bar(self,request,projectid, sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,projectid,ProjectIssuePath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    
   
        
    
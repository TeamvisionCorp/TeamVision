#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.project.pagefactory.project_pageworker import ProjectPageWorker
from doraemon.project.viewmodels.project_left_nav_bar import ProjectForTestingLeftNavBar
from doraemon.project.viewmodels.project_sub_nav_bar import ProjectFortestingSubNavBar
from doraemon.project.pagefactory.project_template_path import ProjectFortestingPath
from doraemon.project.viewmodels.project_fortesting_list_view import ProjectFortestingList
from doraemon.project.viewmodels.vm_project_fortesting import VM_ProjectForTesting
from doraemon.project.models import TestApplication
from doraemon.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from doraemon.project.pagefactory.project_settings_pageworker import ProjectSettingsPageWorker
from business.project.fortesting_service import ForTestingService
from business.auth_user.user_service import UserService
from doraemon.project.viewmodels.vm_project_fortesting_tester import VM_FortestingTester


class ProjectForTestingPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.left_nav_bar_model=ProjectForTestingLeftNavBar
        self.subpage_model=ProjectFortestingSubNavBar
    
    def get_index_page(self,request,projectid, sub_nav_action):
        sub_leftnav=self.get_fortesting_sub_navbar(request,projectid,sub_nav_action)
        left_nav_bar=self.get_fortesting_left_bar(request,projectid,sub_nav_action)
        dm_fortestings=ForTestingService.get_project_fortestings(projectid)
        fortesting_list=self.get_fortesting_list_page(True,False,dm_fortestings)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_leftnav':sub_leftnav,'fortesting_list':fortesting_list}
        return self.get_full_page_with_header(request, pagefileds, projectid,'fortesting/project_fortesting_index.html')
    
    
    
    def get_edit_page(self,request,projectid, fortesting_id):
        sub_leftnav=self.get_fortesting_sub_navbar(request,projectid,"")
        left_nav_bar=self.get_fortesting_left_bar(request,projectid,"all")
        fortesting_edit_controll=self.get_edit_controll(request,projectid,fortesting_id)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_leftnav':sub_leftnav,'fortesting_edit_controll':fortesting_edit_controll}
        return self.get_full_page_with_header(request, pagefileds, projectid,'fortesting/project_fortesting_index.html')
    
    
    
    def get_edit_controll(self,request,projectid, fortesting_id):
        dm_fortesting=TestApplication.objects.get(fortesting_id)
        vm_fortesting=VM_ProjectForTesting(dm_fortesting)
        fortesting_form_controll=self.get_fortesting_form_controll(request,projectid,vm_fortesting)
        pagefileds={'editform':fortesting_form_controll}
        return self.get_webpart(pagefileds,ProjectFortestingPath.fortesting_edit_page_path)
    
    
    
    def get_fortesting_create_dialog(self,request,projectid,testApplicationID):
        if testApplicationID=="0":
            is_create=True
            dm_fortesting=TestApplication()
            vm_fortesting=VM_ProjectForTesting(dm_fortesting,is_create)
            form_html=self.get_fortesting_form_controll(request,projectid,vm_fortesting)
        else:
            is_create=False
            dm_fortesting=TestApplication.objects.get(int(testApplicationID))
            vm_fortesting=VM_ProjectForTesting(dm_fortesting,is_create)
            form_html=self.get_fortesting_form_content(request, projectid, vm_fortesting)
        pagefileds={'formhtml':form_html,"is_create":is_create}
        return self.get_webpart(pagefileds,ProjectFortestingPath.fortesting_create_dialog_path)
    
    
    def get_fortesting_view_part(self,request,fortesting_id,is_edit):
        dm_fortesting=TestApplication.objects.get(int(fortesting_id))
        vm_fortesting=VM_ProjectForTesting(dm_fortesting)
        if is_edit:
            return self.get_fortesting_form_controll(request,dm_fortesting.ProjectID, vm_fortesting)
        else:
            return self.get_fortesting_form_content(request,dm_fortesting.ProjectID, vm_fortesting)
        
        
    
    
    
    def get_fortesting_form_controll(self,request,projectid,vm_fortesting):
        project_dorpdownlist=ProjectCommonControllPageWorker.get_myproject_dropdown_list(self, request, projectid)
        module_dorpdownlist=ProjectCommonControllPageWorker.get_module_dropdown_list(self, projectid, vm_fortesting.fortesting.ProjectModuleID)
        version_dorpdownlist=ProjectCommonControllPageWorker.get_version_dropdown_list(self,projectid)
        pagefileds={'fortesting':vm_fortesting,"module_dorpdownlist":module_dorpdownlist,"project_dorpdownlist":project_dorpdownlist}
        pagefileds['version_dorpdownlist']=version_dorpdownlist
        return self.get_webpart(pagefileds, ProjectFortestingPath.fortesting_create_form_path)
    
    def get_fortesting_form_content(self,request,projectid,vm_fortesting):

        member_menu=self.get_fortesting_tester_menu(projectid,request.user,"member",vm_fortesting.fortesting)
        pagefileds={'fortesting':vm_fortesting,"member_menu":member_menu}
        return self.get_webpart(pagefileds, ProjectFortestingPath.fortesting_content)
    
    
    def get_fortesting_tester_menu(self,projectid,login_user,menu_role,fortesting):
        users=list()
        for user in UserService.all_users():
            if fortesting!=None:
                tmp_user=VM_FortestingTester(projectid,user,None,login_user,fortesting)
                users.append(tmp_user)
        pagefileds={"members":users,"menu_role":menu_role}
        return self.get_webpart(pagefileds, ProjectFortestingPath.fortesting_tester_menu)
    
    
    def get_fortesting_confirm_dialog(self):
        return self.get_webpart_none_args(ProjectFortestingPath.fortesting_confirm_dialog)    
        
    
    def get_fortesting_left_bar(self,request,projectid, sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,projectid,ProjectFortestingPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_fortesting_sub_navbar(self,request,projectid, sub_nav_action):
        fortestings=ForTestingService.get_project_fortestings(projectid)
        return self.get_sub_nav_bar(request, self.subpage_model, projectid,ProjectFortestingPath.sub_nav_template_path,sub_nav_action=sub_nav_action,fortestings=fortestings)
    
    def get_fortesting_list_page(self,fullpart,isversion,fortestings):
        fortesting_list_controll=self.get_fortesting_columns_controll(fortestings)
        context_fileds={'fortesting_list_controll':fortesting_list_controll,"columns":True}
        return self.get_webpart(context_fileds,ProjectFortestingPath.fortesting_list_page_path)
    
    def get_fortesting_list_controll(self,fullpart,isversion,fortestings):
        page=ProjectFortestingList(fullpart,isversion,self.get_fortestings(fortestings))
        context_fileds={'page':page}
        return self.get_webpart(context_fileds,ProjectFortestingPath.fortesting_list_controll_path)
    
     
    def get_fortesting_columns_controll(self,fortestings):
        wait_for_commit=self.get_fortesting_columns_items(fortestings,1)
        commited=self.get_fortesting_columns_items(fortestings,2)
        intesting=self.get_fortesting_columns_items(fortestings,3)
        testfinished=self.get_fortesting_columns_items(fortestings,4)
        archived=self.get_fortesting_columns_items(fortestings,5)
        context_fileds={'wait_for_commit':wait_for_commit}
        context_fileds['commited']=commited
        context_fileds['intesting']=intesting
        context_fileds['testfinished']=testfinished
        context_fileds['archived']=archived
        
        return self.get_webpart(context_fileds,ProjectFortestingPath.fortesting_column_controll_path)
    
    def get_fortesting_columns_items(self,fortestings,item_status):
        result=list()
        if str(item_status)=="1":
            order_by="-id"
        if str(item_status)=="2":
            order_by="-CommitTime"
        if str(item_status)=="3":
            order_by="-TestingStartDate"
        if str(item_status)=="4":
            order_by="-TestingFinishedDate"
        if str(item_status)=="5":
            order_by="-id"
        dm_fortesting_list=fortestings.filter(Status=item_status).order_by(order_by)
        if str(item_status)=="5":
            dm_fortesting_list = dm_fortesting_list[0:30]
        for item in dm_fortesting_list:
            temp=VM_ProjectForTesting(item)
            result.append(temp)
        context_fileds={'fortestings':result}
        return self.get_webpart(context_fileds,ProjectFortestingPath.fortesting_column_item)
    
    
    
    
    def get_fortestings(self,dm_fortestings):
        vm_fortesting_list=list()
        for dm_fortesting in dm_fortestings:
            tmp_fortesting=VM_ProjectForTesting(dm_fortesting)
            vm_fortesting_list.append(tmp_fortesting)
        return vm_fortesting_list
    

        
    
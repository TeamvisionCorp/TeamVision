#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

from doraemon.project.pagefactory.project_pageworker import ProjectPageWorker
from doraemon.project.viewmodels.project_left_nav_bar import ProjectTaskLeftNavBar
from doraemon.project.viewmodels.project_sub_nav_bar import ProjectTaskSubNavBar
# from doraemon.project.viewmodels.project_task_list_view import ProjectTaskList
from doraemon.project.viewmodels.vm_project_task import VM_ProjectTask
from doraemon.project.viewmodels.vm_tag import VM_Tag
from doraemon.project.viewmodels.vm_task_owner import VM_TaskOwner
from doraemon.project.models import Task,ProjectMember
from doraemon.project.pagefactory.project_template_path import ProjectTaskPath
from business.project.task_service import TaskService
from business.project.memeber_service import MemberService
from business.auth_user.user_service import UserService
from doraemon.project.viewmodels.vm_project_member import VM_ProjectMember



class ProjectTaskPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.pagemodel=ProjectTaskLeftNavBar
        self.subpage_model=ProjectTaskSubNavBar
    
    def get_project_task_full_page(self,request,projectid,start_index,sub_nav_action):
        owner=0
        if sub_nav_action.upper()=="CREATEBYME" or sub_nav_action.upper()=="ASGINME":
            owner=request.user.id
        task_list=TaskService.project_all_tasks(owner,projectid,sub_nav_action)
        page_index=[start_index,start_index+10]
        sub_leftnav=self.get_task_sub_navbar(request,projectid,task_list,sub_nav_action)
        task_list_webpart=self.get_task_list_webpart(task_list,page_index)
        left_nav_bar=self.get_task_left_bar(request,projectid,sub_nav_action)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_leftnav':sub_leftnav,'task_list':task_list_webpart}
        return self.get_full_page_with_header(request, pagefileds, projectid,"task/project_task_index.html")

    
    def get_task_left_bar(self,request,projectid, sub_nav_action):
        return self.get_left_nav_bar(request,self.pagemodel,projectid,ProjectTaskPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_task_sub_navbar(self,request,projectid,task_list,sub_nav_action):
        vm_members=list()
        for member in ProjectMember.objects.get_members(projectid):
            user=UserService.get_user(member.PMMember)
            tmp_member=VM_ProjectMember(0,user,0,None)
            vm_members.append(tmp_member)
        return self.get_sub_nav_bar(request, self.subpage_model, projectid,ProjectTaskPath.sub_nav_template_path,sub_nav_action=sub_nav_action,tasks=task_list,members=vm_members)
    
    def get_task_list_webpart(self,task_list,page_index,full_part=True,show_user=True,show_tag=True):
        page_tasks=task_list[page_index[0]:page_index[1]]
        task_list_controll=self.get_task_listcontrol(page_tasks,full_part,show_user,show_tag)
        context_fileds={'task_listcontroll':task_list_controll,"is_project_page":show_user,"task_length":len(task_list)}
        return self.get_webpart(context_fileds,ProjectTaskPath.task_page_template_path)
    

    
    def get_more_tasks(self,request,projectid,filters,owner,start_index):
        task_list=TaskService.project_tasks_byowner(request,projectid,owner,filters)[start_index:start_index+8]
        return self.get_task_listcontrol(task_list,True,False,True)
    
    def get_owner_tasks(self,request,project_id,filters,owner):
        task_list=TaskService.project_tasks_byowner(request,project_id,owner,filters)[0:8]
        task_page_worker=ProjectTaskPageWorker(request)
        return task_page_worker.get_task_listcontrol(task_list,True,False,True)
        
    
    def get_task_listcontrol(self,task_list,page_fullpart=True,show_user=True,show_tag=True):
        tasks=self.get_tasks(task_list, page_fullpart, show_user, show_tag)
        context_fileds={'tasks':tasks}
        return self.get_webpart(context_fileds,ProjectTaskPath.task_list_template_path)
    
    def get_task_edit_page(self,request,projectid,taskid):
        dm_task=Task.objects.get(taskid)
        sub_leftnav=self.get_task_sub_navbar(request,projectid,None,"")
        tag_menu=self.get_task_tag_menu(dm_task,"tag")
        owners=UserService.all_users()
        owner_menu=self.get_task_owner_menu(dm_task,owners,request.user,"member")
        task=VM_ProjectTask(dm_task,tag_menu,owner_menu,None,False)
        pagefileds={"task":task,"taskoption":self.get_task_option(task)}
        task_edit_part=self.get_webpart(pagefileds,ProjectTaskPath.task_edit_template_path)
        left_nav_bar=self.get_task_left_bar(request,projectid,"all")
        pagefileds={'left_nav_bar':left_nav_bar,'sub_leftnav':sub_leftnav,'task_edit_part':task_edit_part}
        return self.get_full_page_with_header(request, pagefileds, projectid,"task/project_task_index.html")
    
    
    def get_task_create_dialog(self,request):
        dm_task=Task()
        tag_menu=self.get_task_tag_menu(dm_task,"tag")
        owners=UserService.all_users()
        owner_menu=self.get_task_owner_menu(dm_task,owners,request.user,"member")
        project_menu=self.get_project_menu(request,ProjectTaskPath.project_menu_template_path)
        task=VM_ProjectTask(dm_task,tag_menu,owner_menu,project_menu,True)
        pagefileds={"taskoption":self.get_task_option(task)}
        return self.get_webpart(pagefileds,ProjectTaskPath.project_task_create_dialog)
    
    def get_task_option(self,task):
        pagefileds={"task":task}
        task_edit_part=self.get_webpart(pagefileds,ProjectTaskPath.task_option_template_path)
        return task_edit_part
        
        
    
    def get_task_tag_menu(self,task,taskrole):
        tags=list()
        for tag in TaskService.all_tags():
            tmp_tag=VM_Tag(tag,task.Tags)
            tags.append(tmp_tag)
        context_fileds={'tags':tags,'tagrole':taskrole}
        return self.get_webpart(context_fileds,ProjectTaskPath.tag_menu_template_path)
    
    def get_task_owner_menu(self,task,owners,login_user,menu_role):
        users=list()
        for user in owners:
            tmp_user=VM_TaskOwner(task,user,login_user)
            users.append(tmp_user)
        pagefileds={"owners":users,"menu_role":menu_role}
        return self.get_webpart(pagefileds, ProjectTaskPath.owner_menu_template_path)
        
    
    def get_tasks(self,all_tasks,page_fullpart=True, show_user=True, show_tag=True):
        task_list=list()
        for dm_task in all_tasks:
            tag_menu=self.get_task_tag_menu(dm_task,"tag-inline")
            owners=MemberService.get_member_users(dm_task.ProjectID)
            owner_menu=self.get_task_owner_menu(dm_task,owners,None,"member-inline")
            tmp_task=VM_ProjectTask(dm_task,tag_menu,owner_menu,None,False,page_fullpart, show_user, show_tag)
            task_list.append(tmp_task)
        return task_list
        
        
    
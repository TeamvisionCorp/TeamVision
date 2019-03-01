# coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.home.pagefactory.pageworker import DevicePageWorker
from teamvision.home.viewmodels.home_left_nav_bar import HomeTaskLeftNavBar
from teamvision.home.viewmodels.home_sub_nav_bar import HomeTaskSubNavBar
from teamvision.home.pagefactory.home_template_path import HomeTaskPath
from teamvision.project.pagefactory.project_task_pageworker import ProjectTaskPageWorker
from business.project.task_service import TaskService
from business.auth_user.user_service import UserService
from teamvision.project.viewmodels.vm_project_member import VM_ProjectMember


class HomeTaskPageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.side_bar_model = HomeTaskLeftNavBar
        self.sub_side_bar_model = HomeTaskSubNavBar

    def get_full_page(self, request, start_index, sub_nav_action):
        owner = 0
        if sub_nav_action.upper() == "CREATEBYME" or sub_nav_action.upper() == "ASGINME":
            owner = request.user.id
        task_list = TaskService.all_my_tasks(request, sub_nav_action, owner)
        page_index = [start_index, start_index + 8]
        sub_leftnav = self.get_task_sub_navbar(request, task_list, sub_nav_action)
        left_nav_bar = self.get_task_left_bar(request, sub_nav_action)
        task_page_worker = ProjectTaskPageWorker(request)
        task_list_webpart = task_page_worker.get_task_list_webpart(task_list, page_index, True, False, True)
        page_fileds = {'left_nav_bar': left_nav_bar, 'sub_leftnav': sub_leftnav, 'task_list': task_list_webpart}
        return self.get_page(page_fileds, HomeTaskPath.task_index_path, request)

    def get_task_left_bar(self, request, sub_nav_action):
        return self.get_left_nav_bar(request, self.side_bar_model, HomeTaskPath.left_nav_template_path,
                                     sub_nav_action=sub_nav_action)

    def get_task_sub_navbar(self, request, task_list, sub_nav_action):
        task_list = TaskService.all_my_tasks(request, sub_nav_action, 0)
        owner_id_list = list()
        vm_members = list()
        for task in task_list:
            temp_list = eval(task.Owner)
            for owner in temp_list:
                if owner != "" and owner not in owner_id_list:
                    owner_id_list.append(owner)
        for owner_id in owner_id_list:
            member = UserService.get_user(int(owner_id))
            tmp_member = VM_ProjectMember(0, member, 0, None)
            vm_members.append(tmp_member)
        return self.get_left_nav_bar(request, self.sub_side_bar_model, HomeTaskPath.sub_nav_template_path,
                                     sub_nav_action=sub_nav_action, tasks=task_list, members=vm_members)

    def get_more_tasks(self, request, filters, owner, start_index):
        task_list = TaskService.project_tasks_byowner(request, 0, owner, filters)[start_index:start_index + 8]
        task_page_worker = ProjectTaskPageWorker(request)
        return task_page_worker.get_task_listcontrol(task_list, True, False, True)

    def get_owner_tasks(self, request, project_id, filters, owner):
        task_list = TaskService.project_tasks_byowner(request, project_id, owner, filters)[0:8]
        task_page_worker = ProjectTaskPageWorker(request)
        return task_page_worker.get_task_listcontrol(task_list, True, False, True)

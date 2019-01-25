# coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''

from teamvision.project.models import Task
from gatesidelib.common.simplelogger import SimpleLogger
from gatesidelib.datetimehelper import DateTimeHelper
from business.project.project_service import ProjectService
from teamvision.project.models import Tag
from django.contrib.admin.models import DELETION, CHANGE, ADDITION
import pytz,datetime
from teamvision.settings import  TIME_ZONE


class TaskService(object):
    '''
    classdocs
    '''

    @staticmethod
    def all_tasks(request, filters):
        return TaskService.project_all_tasks(request.user.id, 0, filters)

    @staticmethod
    def all_my_tasks(request, filters, owner):
        my_project_ids = list()
        my_products = ProjectService.get_products_include_me(request).order_by('-id')
        for product in my_products:
            projects = ProjectService.get_projects_include_me(request, str(product.id)).order_by('-id')
            my_project_ids.extend([project.id for project in projects])
        result = TaskService.project_all_tasks(owner, my_project_ids, filters)
        return result

    @staticmethod
    def project_all_tasks(owner, projectid, filters):
        result = list()
        if filters.upper() == "ALL":
            result = TaskService.tasks_byfilter(owner, projectid, None, None, False, False).order_by('-id')
        if filters.upper() == "PROCESS":
            result = TaskService.tasks_byfilter(owner, projectid, 0, None, False, False).order_by('-id')
        if filters.upper() == "CREATEBYME":
            result = TaskService.tasks_byfilter(owner, projectid, None, None, True, False).order_by('-id')
        if filters.upper() == "ASGINME":
            result = TaskService.tasks_byfilter(owner, projectid, None, None, False, True).order_by('-id')
        return result

    @staticmethod
    def project_tasks_byowner(request, projectid, owner, filters):
        if str(projectid) != "0":
            result = TaskService.project_all_tasks(owner, projectid, filters)
        else:
            if str(owner) != "0":
                result = TaskService.all_my_tasks(request, filters, owner)
            else:
                result = TaskService.all_my_tasks(request, filters, 0)
        return result

    @staticmethod
    def all_tags():
        return Tag.objects.all().filter(TagType=1)

    @staticmethod
    def project_tasks_byfilter(request, projectid, taskfilter):
        result = TaskService.project_tasks(request, projectid)
        if taskfilter.upper() == "FINISHED":
            pass
        return result

    @staticmethod
    def tasks_byfilter(owner, projectids, task_status, task_tags, is_created, joined):
        if isinstance(projectids, list):
            result = Task.objects.all().filter(ProjectID__in=projectids)
        else:
            result = Task.objects.all().filter(ProjectID=int(projectids))

        if is_created:
            result = result.filter(Creator=owner)

        if str(owner) != "0":
            result = result.filter(Owner=owner)
        if task_status != None:
            result = result.filter(Status=task_status)

        if task_tags:
            result = result.filter(Tags__contains=task_tags)
        return result.order_by('-id')

    @staticmethod
    def tasks_pagination(tasks, page_index, count_per_page):
        start_index = (page_index - 1) * count_per_page
        end_index = page_index * count_per_page
        return tasks[start_index:end_index]

    @staticmethod
    def create_task(task_data,user):
        try:
            task = Task()
            task = TaskService.init_task(task_data,task,user.id)
            task.Creator = int(user.id)
            task.Status = 0
            task.Parent = None
            task.save()
            for child in task_data.get('childTask').get('items',[]):
                TaskService.create_child_task(task,child)
            TaskService.log_create_activity(user, task)
            return task
        except Exception as ex:
            SimpleLogger.exception(ex)

    @staticmethod
    def create_child_task(parent_task,child):
        try:
            if child.get('value') and child.get('value').strip() != '':
                task = Task()
                task.Title = child.get('value')
                task.Status = child.get('status')
                task.IsActive = child.get('active')
                task.Parent = parent_task
                task.ProjectID = parent_task.ProjectID
                task.Description = ''
                task.DeadLine = parent_task.DeadLine
                task.Owner = parent_task.Owner
                task.WorkHours = 0
                task.Priority = 3
                task.Creator = parent_task.Creator
                task.Progress = 0
                task.save()
        except Exception as ex:
            SimpleLogger.exception(ex)


    @staticmethod
    def edit_task(task,task_data, user):
        try:
            task = TaskService.init_task(task_data,task,user.id)
            task.save()
            TaskService.edit_child_task(task,task_data.get('childTask'))
            TaskService.log_change_activity(user, task)
        except Exception as ex:
            SimpleLogger.exception(ex)

    @staticmethod
    def edit_child_task(parent_task,child_data):
        for child in child_data.get('items',[]):
            try:
                if child.get('value').strip() != '':
                    task_id = child.get('id')
                    if task_id:
                        child_task = Task.objects.get(int(task_id))
                        if child_task:
                            child_task.Title = child.get('value')
                            child_task.Status = child.get('status')
                            child_task.IsActive = child.get('active')
                            child_task.save()
                    else:
                        TaskService.create_child_task(parent_task,child)
            except Exception as ex:
                SimpleLogger.exception(ex)
                continue

    @staticmethod
    def delete_task(request, taskid):
        task = Task.objects.get(taskid)
        task.IsActive = 0
        task.save()
        TaskService.log_delete_activity(request.user, task)

    @staticmethod
    def update_property(request, taskid):
        task = Task.objects.get(taskid)
        task.Progress = request.POST.get("Progress")
        task.Title = request.POST.get("Title")
        task.WorkHours = request.POST.get("WorkHours")
        task.Tags = request.POST.get("Tags")
        task.DeadLine = request.POST.get("DeadLine")
        task.Status = request.POST.get("Status")
        task.Description = request.POST.get("Description")
        task.Owner = request.POST.get("Owner")
        update_fields = list()
        for field in request.POST:
            update_fields.append(field)
        if task.Progress == 100:
            task.Status = 1
            update_fields.append('Status')
        task.save(update_fields=update_fields)
        TaskService.log_change_property_activity(request.user, Task.objects.get(taskid), update_fields[0])

    @staticmethod
    def init_task(task_data,task,user_id):
        tmp_task = task
        for field in  tmp_task.__dict__.keys():
            if field in task_data.keys():
                if field == 'id':
                    continue
                if field == 'DeadLine':
                    dead_line = task_data.get('DeadLine')
                    if "000Z" in dead_line:
                        temp_date = datetime.datetime.strptime(dead_line, "%Y-%m-%dT%H:%M:%S.000Z")
                        ts = int(temp_date.timestamp())
                        temp_date = datetime.datetime.fromtimestamp(ts, pytz.timezone(TIME_ZONE))
                        offset = temp_date.tzinfo.utcoffset(temp_date)
                        temp_date = temp_date+ datetime.timedelta(seconds=offset.seconds)
                    else:
                        temp_date = dead_line

                    if dead_line == "":
                        tmp_task.DeadLine = DateTimeHelper.add_day(DateTimeHelper.get_now_date(),1)
                    else:
                        tmp_task.DeadLine = temp_date
                    continue
                if field == 'Owner':
                    owner = task_data.get('Owner')
                    if str(owner) == "0":
                        owner = user_id
                    tmp_task.Owner = owner
                    continue
                if field == 'ProjectID':
                    project = task_data.get('ProjectID')[0]
                    version = task_data.get('ProjectID')[1]
                    tmp_task.ProjectID = project
                    tmp_task.Version = version
                    continue
                tmp_task.__setattr__(field,task_data.get(field))
        tmp_task.Progress = 0
        tmp_task.StartDate =None
        return tmp_task



    @staticmethod
    def log_create_activity(user, target):
        Task.objects.log_action(user.id, target.id, target.Title, ADDITION, "创建了新任务", target.ProjectID)

    @staticmethod
    def log_delete_activity(user, target):
        Task.objects.log_action(user.id, target.id, target.Title, DELETION, "删除了任务", target.ProjectID)

    @staticmethod
    def log_change_activity(user, target):
        Task.objects.log_action(user.id, target.id, target.Title, CHANGE, "修改了任务", target.ProjectID)

    @staticmethod
    def log_change_property_activity(user, target, filed_name):
        if filed_name == "Status":
            Task.objects.log_action(user.id, target.id, target.Title, CHANGE, "更新了任务状态", target.ProjectID)
        elif filed_name == "DeadLine":
            Task.objects.log_action(user.id, target.id, target.Title, CHANGE, "修改了任务截止日期", target.ProjectID)
        elif filed_name == "Progress":
            Task.objects.log_action(user.id, target.id, target.Title, CHANGE, "更新了任务进度", target.ProjectID)
        else:
            Task.objects.log_action(user.id, target.id, target.Title, CHANGE, "修改了任务信息", target.ProjectID)

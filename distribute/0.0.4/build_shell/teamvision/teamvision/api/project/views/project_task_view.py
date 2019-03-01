# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from rest_framework import generics,status, response
from teamvision.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from teamvision.project import models
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from teamvision.api.project.filters import project_filter
from teamvision.api.project.filters.project_pagination import ProjectPagination
from business.project.task_service import TaskService
from json.decoder import JSONDecoder


class ProjectTaskListView(generics.ListCreateAPIView):
    """
    get:
    /api/project/project_id/project_tasks
    get task list with project_id  FilterSet: Null FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull

    post:
        create new task
    """
    serializer_class = project_serializer.ProjectTaskSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = ProjectPagination


    def get_queryset(self):
        project_id = int(self.kwargs['project_id'])
        version_id = int(self.kwargs['version_id'])
        if str(project_id)!='0':
            if str(version_id)!='0':
                qs=models.Task.objects.get_tasks(project_id).filter(Version=int(version_id)).order_by('Priority', 'id')
            else:
                qs=models.Task.objects.get_tasks(project_id).order_by('Priority', 'id')
        else:
            qs=TaskService.all_my_tasks(self.request,'ALL',self.request.user.id)
        owners=self.request.GET.get("Owner__in",None)
        if owners is not None:
            if ',' in owners:
                owner_tasks = models.ProjectTaskOwner.objects.all().filter(Owner__in=eval(owners))
            else:
                owner_tasks = models.ProjectTaskOwner.objects.all().filter(Owner=int(owners))
            owner_task_ids=[task.Task for task in owner_tasks]
            qs = qs.filter(id__in=owner_task_ids)
        return project_filter.ProjectTaskFilterSet(data=self.request.GET, queryset=qs).filter()

    def post(self, request, *args, **kwargs):
        form_data = request.POST.get('models',None)
        if form_data == None:
            validate_data = request.data
        else:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
        task = TaskService.create_task(validate_data,request.user)
        serializer = project_serializer.ProjectTaskSerializer(instance=task,data=validate_data)
        serializer.is_valid(raise_exception=True    )
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PorjectTaskView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/task/task_id
    get,update,delete task with taskid
    """
    serializer_class = project_serializer.ProjectTaskSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        form_data = self.request.POST.get('models',None)
        if form_data != None:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
            task_id = int(validate_data.get('id',0))
        else:
            task_id = int(self.kwargs['task_id'])
        task=models.Task.objects.get(task_id)
        return task



    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        form_data = request.POST.get('models', None)
        if form_data == None:
            validate_data = request.POST or request.data
        else:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
        task  = self.get_object()
        TaskService.edit_task(task,validate_data,request.user)
        serializer = self.get_serializer(task, data=validate_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(task, '_prefetched_objects_cache', None):
            task._prefetched_objects_cache = {}
        return response.Response(serializer.data)


    def perform_destroy(self, instance):
        TaskService.delete_task(self.request,instance.id)

class ProjectTaskOwnerListView(generics.ListCreateAPIView):
    """
    get:
    /api/project/task/<task_id>/task_owners
    get task owner list with task_id  FilterSet: Null FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull

    post:
        create new task
    """
    serializer_class = project_serializer.ProjectTaskOwnerSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = ProjectPagination


    def get_queryset(self):
        task_id = int(self.kwargs.get('task_id',0))
        if task_id != 0:
            qs = models.ProjectTaskOwner.objects.get_owners(task_id)
        else:
            qs = models.ProjectTaskOwner.objects.all()
        return project_filter.ProjectTaskOwnerFilterSet(data=self.request.GET,queryset=qs).filter()

    def post(self, request, *args, **kwargs):
        form_data = request.POST.get('models',None)
        if form_data == None:
            validate_data = request.data
        else:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
        task_id = validate_data.get('Task')
        task = models.Task.objects.get(int(task_id))
        owner = validate_data.get('Owner')
        unit = validate_data.get('Unit')
        task_owner = TaskService.create_task_owner(task,owner,unit)
        serializer = project_serializer.ProjectTaskOwnerSerializer(instance=task_owner,data=validate_data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PorjectTaskOwnerView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/task_owner/id
    get,update,delete task owner with id
    """
    serializer_class = project_serializer.ProjectTaskOwnerSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        form_data = self.request.POST.get('models',None)
        if form_data != None:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
            task_owner_id = int(validate_data.get('id',0))
        else:
            task_owner_id = int(self.kwargs['id'])
        task_owner=models.ProjectTaskOwner.objects.get(task_owner_id)
        return task_owner

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        form_data = request.POST.get('models', None)
        if form_data == None:
            validate_data = request.POST or request.data
        else:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)

        task_owner_id = validate_data.get('id')
        unit = validate_data.get('Unit')
        task_owner = TaskService.edit_task_owner(task_owner_id,unit )
        serializer = self.get_serializer(instance=task_owner, data=validate_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(task_owner, '_prefetched_objects_cache', None):
            task_owner._prefetched_objects_cache = {}
        # return response.Response({'1':1})
        return response.Response(serializer.data)

    def perform_destroy(self, instance):
        form_data = self.request.POST.get('models', None)
        if form_data != None:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
            task_owner_id = int(validate_data.get('id', 0))
        else:
            task_owner_id = int(self.kwargs['id'])
        TaskService.delete_task_owner(int(task_owner_id))


class ProjectTaskDependencyListView(generics.ListCreateAPIView):
    """
    get:
    /api/project/task/<task_id>/task_dependency
    get task owner list with task_id  FilterSet: Null FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull

    post:
        create new task
    """
    serializer_class = project_serializer.ProjectTaskDependencySerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = ProjectPagination

    def get_queryset(self):
        task_id = int(self.kwargs.get('task_id',0))
        if task_id != 0:
            qs = models.ProjectTaskDependency.objects.get_task_dependency(task_id)
        else:
            qs = models.ProjectTaskDependency.objects.all()

        return project_filter.ProjectTaskDependencyFilterSet(data=self.request.GET,queryset=qs).filter()


    def post(self, request, *args, **kwargs):
        form_data = request.POST.get('models',None)
        if form_data == None:
            validate_data = request.data
        else:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
        task_dependency = TaskService.create_task_dependency(validate_data)
        serializer = project_serializer.ProjectTaskDependencySerializer(instance=task_dependency,data=validate_data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PorjectTaskDependencyView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/project/task_dependency/id
    get,update,delete task dependency with id
    """
    serializer_class = project_serializer.ProjectTaskDependencySerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        form_data = self.request.POST.get('models',None)
        if form_data != None:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
            task_dependency_id = int(validate_data.get('id',0))
        else:
            task_dependency_id = int(self.kwargs['id'])
        task_dependency=models.ProjectTaskDependency.objects.get(task_dependency_id)
        return task_dependency


    def perform_destroy(self, instance):
        form_data = self.request.POST.get('models', None)
        if form_data != None:
            json_decoder = JSONDecoder()
            validate_data = json_decoder.decode(form_data)
            task_dependency_id = int(validate_data.get('id', 0))
        else:
            task_dependency_id = int(self.kwargs['id'])
        TaskService.delete_task_dependency(int(task_dependency_id))
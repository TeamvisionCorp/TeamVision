#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.home.models import TaskQueue
from rest_framework import generics,response
from teamvision.ci.models import CITaskHistory
from teamvision.api.common.serializer import task_queue_serializer
from rest_framework.permissions import AllowAny
from business.ci.ci_task_history_service import  CITaskHistoryService
from business.ci.ci_task_queue_service import  CITQService
from business.ci.ci_task_service import CITaskService
from teamvision.api.common.filters.taskqueue_filter import TaskQueueFilterSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication

class TaskQueueListView(generics.ListCreateAPIView):
    """
    /api/common/task_queues
    UrlFilterSet:'AgentID','Status','TaskID','TaskType','Command','IsLocked','TaskUUID'
    Command: 1,2
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=
    """
    serializer_class =task_queue_serializer.TaskQueueSerializer
    permission_classes=[AllowAny]
    queryset=TaskQueue.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    

    def get_queryset(self):
        qs = super(TaskQueueListView, self).get_queryset()
        return TaskQueueFilterSet(data=self.request.GET, queryset=qs).filter()


class TaskQueueView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = task_queue_serializer.TaskQueueSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        print(1)
        tq_id =int(self.kwargs['id'])
        return TaskQueue.objects.get(tq_id)


class TaskQueueDoneView(generics.RetrieveAPIView):
    """
     /api/common/task_queue/<id>/done

    """
    serializer_class = task_queue_serializer.TaskQueueSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        tq_id = int(self.kwargs['id'])
        return TaskQueue.objects.get(tq_id)

    def get(self, request, *args, **kwargs):
        message = "success"
        try:
            print(self.request.GET)
            status = self.request.GET.get('status',5)
            build_message = self.request.GET.get('error_msg','')
            task_queue = self.get_object()
            CITaskHistoryService.save_build_log(str(task_queue.id),True)
            CITQService.update_task_queue_status(task_queue.id,status,build_message)
            CITaskService.send_task_enqueue_message()
        except Exception as ex:
            print(ex)
            message = str(ex)
        return response.Response({"message":message})




    

    
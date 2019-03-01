#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.home.models import TaskQueue
from rest_framework import generics
from teamvision.api.common.serializer import task_queue_serializer
from rest_framework.permissions import AllowAny
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
        ta_id =int(self.kwargs['id'])
        return TaskQueue.objects.get(ta_id)
    

    
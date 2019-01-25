#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from doraemon.home.models import TaskQueue
from url_filter.filtersets.django import ModelFilterSet

class TaskQueueFilterSet(ModelFilterSet):
    class Meta(object):
        model = TaskQueue
        fields = ['AgentID','Status','TaskID','TaskType','Command','IsLocked','TaskUUID']


        
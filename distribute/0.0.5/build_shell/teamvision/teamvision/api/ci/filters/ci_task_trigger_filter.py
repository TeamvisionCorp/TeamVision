#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.ci.models import CITaskApiTrigger
from url_filter.filtersets.django import ModelFilterSet


class CITaskTriggerFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITaskApiTrigger
        fields = ['id','TaskID','TaskQueueUUID','ActionType','IsActive']


        
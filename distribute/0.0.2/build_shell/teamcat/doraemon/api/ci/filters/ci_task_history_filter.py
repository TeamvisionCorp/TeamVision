#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from doraemon.ci.models import CITaskHistory
from url_filter.filtersets.django import ModelFilterSet

class CITaskHistoryFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITaskHistory
        fields = ['id','CITaskID','TaskQueueID','TaskUUID']


        
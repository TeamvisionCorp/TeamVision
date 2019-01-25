# coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''

from doraemon.ci.models import AutoTestingTaskResult
from url_filter.filtersets.django import ModelFilterSet


class AutoTestingResultFilterSet(ModelFilterSet):
    class Meta(object):
        model = AutoTestingTaskResult
        fields = ['TaskHistoryID', 'TaskUUID']

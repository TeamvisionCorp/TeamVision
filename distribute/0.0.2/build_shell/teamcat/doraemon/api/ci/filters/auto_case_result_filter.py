#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from doraemon.ci.models import AutoCaseResult,UnitTestCaseResult
from url_filter.filtersets.django import ModelFilterSet

class AutoCaseResultFilterSet(ModelFilterSet):
    class Meta(object):
        model = AutoCaseResult
        fields = ['TaskResultID','Result']

class UnitTestCaseResultFilterSet(ModelFilterSet):
    class Meta(object):
        model = UnitTestCaseResult
        fields = ['TaskResultID','Result']
        
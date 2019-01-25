#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.project import models
from url_filter.filtersets.django import ModelFilterSet


class IssueFilterSet(ModelFilterSet):
    class Meta(object):
        model = models.ProjectIssue
        fields = ['Project','Version','Title','ProjectPhase', 'Priority' ,'Status','Module','Processor','IssueCategory','Solution','Severity','Creator','CreationTime','ClosedTime','ResolvedTime','Team']
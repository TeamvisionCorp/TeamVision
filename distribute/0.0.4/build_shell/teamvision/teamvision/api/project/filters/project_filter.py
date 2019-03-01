# coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''

from teamvision.project import models
from url_filter.filtersets.django import ModelFilterSet


class ProjectTaskFilterSet(ModelFilterSet):
    class Meta(object):
        model = models.Task
        fields = ['ProjectID', 'Status','Title','Parent','Version']

class ProjectTaskOwnerFilterSet(ModelFilterSet):
    class Meta(object):
        model = models.ProjectTaskOwner
        fields = ['Task','Version']

class ProjectTaskDependencyFilterSet(ModelFilterSet):
    class Meta(object):
        model = models.ProjectTaskOwner
        fields = ['Task','Version']


class ProjectDocumentFilterSet(ModelFilterSet):
    class Meta(object):
        model = models.ProjectDocument
        fields = ['ProjectID','Parent','ReadOnly','Type']


class ProjectFortestingFilterSet(ModelFilterSet):
    class Meta(object):
        model = models.Task
        fields = ['ProjectID', 'Status']

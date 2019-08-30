#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.home.models import Team
from url_filter.filtersets.django import ModelFilterSet

class TeamFilterSet(ModelFilterSet):
    class Meta(object):
        model = Team
        fields = ['Creator']


        
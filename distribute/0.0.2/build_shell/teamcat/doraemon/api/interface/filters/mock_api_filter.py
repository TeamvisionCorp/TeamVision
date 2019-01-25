# coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''

from doraemon.interface.models import MockAPI, MockResponse
from url_filter.filtersets.django import ModelFilterSet


class MockAPIFilterSet(ModelFilterSet):
    class Meta(object):
        model = MockAPI
        fields = ['id','Parent','MockHandler','ApiType','ApiPath','Enable']


class MockResponseFilterSet(ModelFilterSet):
    class Meta(object):
        model = MockResponse
        fields = ['id','ApiID','Enable']

# coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.interface.models import MockAPI, MockResponse


class MockAPISerializer(serializers.ModelSerializer):
    http_method_name = serializers.SerializerMethodField()

    def get_http_method_name(self, obj):

        result = "GET"
        if obj.HttpMethod == 1:
            result = "GET"
        if obj.HttpMethod == 2:
            result = "POST"
        if obj.HttpMethod == 3:
            result = "PUT"
        if obj.HttpMethod == 4:
            result = "PATCH"
        if obj.HttpMethod == 5:
            result = "DELETE"
        return result

    class Meta:
        model = MockAPI
        exclude = ('IsActive', 'CreationTime')
        read_only_fields = ('id',)
        extra_kwargs = {'MockServer': {'required': False},
                        'MatchParten': {'required': False}, 'MockHandler': {'required': False},'ApiPath': {'required': False},
                        'Description': {'required': False,'allow_null':True},
                        'MockResponse': {'required': False}}


class MockAPITreeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="ApiTitle")
    type = serializers.CharField(source="ApiType")
    extend = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_extend(self, obj):
        return True

    def get_children(self, obj):
        return self.child_tree(obj)

    def child_tree(self, obj):
        result = list()
        temp_1 = dict()
        temp_1['title'] = obj.ApiTitle
        temp_1['type'] = obj.ApiType
        temp_1['extent'] = True
        # temp_1['children'] = list()
        if obj.ApiType == 1:
            return result.append(temp_1)
        else:
            child_list = MockAPI.objects.get_children(obj.id)
            for child in child_list:
                temp = dict()
                temp['id'] = child.id
                temp['title'] = child.ApiTitle
                temp['type'] = child.ApiType
                temp['extent'] = True
                temp_children = self.child_tree(child)
                if temp_children:
                    temp['children'] = list()
                    temp['children'].append(temp_children)
                if isinstance(temp_children, list):
                    temp['children'] = list()
                    temp['children'] = temp_children
                result.append(temp)
            return result

    class Meta:
        model = MockAPI
        fields = ('id', 'title', 'type', 'extend', 'children')
        depth = 1


class MockResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockResponse
        exclude = ('IsActive', 'CreationTime')
        read_only_fields = ('id',)
        extra_kwargs = {'CallBackMethod': {'required': False}, 'CallBackUrl': {'required': False}}

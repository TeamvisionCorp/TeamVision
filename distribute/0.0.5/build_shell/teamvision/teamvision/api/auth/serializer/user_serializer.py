#coding=utf-8
'''
Created on 2016-10-12

@author: Administrator
'''

from rest_framework import serializers
from django.contrib.auth.models import User,Group
from business.auth_user.user_service import UserService
from business.ucenter.account_service import AccountService


class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    system_permision = serializers.SerializerMethodField()
    system_role_label = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return AccountService.get_avatar_url(obj)

    def get_system_permision(self, obj):
        return UserService.get_system_permission(obj.id)


    class Meta:
        model = User
        exclude=('password',)
        read_only_fields = ('id',)
        depth=2
    
    def get_name(self, obj):
        return obj.last_name+obj.first_name


    def get_system_role_label(self,obj):
        result = 'U'
        for user_group in obj.groups.get_queryset():
            group=Group.objects.get(id=user_group.id)
            result = group.name[0]
        return result

        
        
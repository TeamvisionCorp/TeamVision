#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from doraemon.home.models import Agent
from rest_framework import generics
from doraemon.api.common.serializer import user_serializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from business.auth_user.user_service import UserService

class UserView(generics.RetrieveAPIView):
    """
    url:/api/common/user/id
    """

    serializer_class = user_serializer.UserSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    

    def get_object(self):
        user_id =int(self.kwargs['id'])
        if str(user_id) == '0':
            return self.request.user
        else:
            return UserService.get_user(user_id)

class UserListView(generics.ListAPIView):
    """
    url:/api/common/user/list
    """

    serializer_class = user_serializer.UserSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return UserService.all_users()
    

    
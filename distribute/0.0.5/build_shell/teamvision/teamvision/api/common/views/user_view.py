#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.home.models import Agent
from rest_framework import generics,status,response
from teamvision.api.common.serializer import user_serializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from business.auth_user.user_service import UserService
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication

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

class UserLoginView(generics.CreateAPIView,generics.DestroyAPIView):
    """
    url:/api/common/user/list
    """

    serializer_class = user_serializer.UserSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


    def post(self, request, *args, **kwargs):
        result = UserService.login(request)
        return response.Response(result, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        UserService.logout(request)
        return response.Response('', status=status.HTTP_204_NO_CONTENT)



    

    
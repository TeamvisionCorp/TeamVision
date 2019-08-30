#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.contrib.auth.models import User
from rest_framework import generics,response,status
from teamvision.api.auth.serializer import user_serializer
from business.auth_user.user_service import UserService
from rest_framework.permissions import AllowAny

from rest_framework.authentication import BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication

class UserListView(generics.ListCreateAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = user_serializer.UserSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return UserService.all_users()

    def post(self, request, *args, **kwargs):
        user = UserService.create_user(request)
        serializer = user_serializer.UserSerializer(instance=user)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = user_serializer.UserSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    

    def get_object(self):
        user_id =int(self.kwargs['id'])
        return UserService.get_user(user_id)



    def post(self, request, *args, **kwargs):
        user_id = int(self.kwargs['id'])
        user = UserService.edit_user(request,user_id)
        serializer = user_serializer.UserSerializer(instance=user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        user_id = int(self.kwargs['id'])
        old_password = request.data.get('oldPassword',None)
        if old_password is None:
            message = UserService.reset_user_password(request,user_id)
        else:
            message = UserService.change_password(request)
        if message is None:
            return response.Response({"message":"密码修改成功"}, status=status.HTTP_200_OK)
        else:
            return response.Response(message, status=status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        user_id = int(self.kwargs['id'])
        user = UserService.update_user_group(request,user_id)
        serializer = user_serializer.UserSerializer(instance=user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        user_id = int(self.kwargs['id'])
        UserService.delete_user(user_id)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    

    
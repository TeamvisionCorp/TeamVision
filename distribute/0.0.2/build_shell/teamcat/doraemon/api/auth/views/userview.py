#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.contrib.auth.models import User
from rest_framework import generics
from doraemon.api.auth.serializer import user_serializer
from rest_framework.permissions import AllowAny

class UserListView(generics.ListCreateAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = user_serializer.UserSerializer
    permission_classes=[AllowAny]
    

    def get_queryset(self):
        return User.objects.all()

class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = user_serializer.UserSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        user_id =int(self.kwargs['id'])
        return User.objects.get(id=user_id)
    

    
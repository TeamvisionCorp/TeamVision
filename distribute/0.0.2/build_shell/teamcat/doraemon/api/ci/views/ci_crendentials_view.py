#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''
from rest_framework import generics
from doraemon.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from doraemon.ci.models import CICredentials
from rest_framework.response import Response




class CICrendentialsView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.CICrendentialsSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        server_id =int(self.kwargs['id'])
        return CICredentials.objects.get(server_id)

class CICrendentialsListView(generics.ListCreateAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.CICrendentialsSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        return CICredentials.objects.all()
    

#     def get_object(self):
#         server_id =int(self.kwargs['id'])
#         return CIServer.objects.get(server_id)
#     def get(self, request, *args, **kwargs):
#         return Response("fdsfds")
    
        
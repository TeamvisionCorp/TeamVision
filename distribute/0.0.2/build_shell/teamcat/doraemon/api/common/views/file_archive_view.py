#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from doraemon.home.models import Agent
from rest_framework import generics
from doraemon.api.common.serializer import agent_serializer
from rest_framework.permissions import AllowAny
from business.common.file_info_service import FileInfoService
from rest_framework.response import Response
from doraemon.home.models import FileInfo
from gatesidelib.common.simplelogger import SimpleLogger

class FileArchiveView(generics.RetrieveAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class =None
    permission_classes=[AllowAny]
    
    
    def get(self, request, *args, **kwargs):
        result="ok"
        try:
            file_id=self.kwargs['file_id']
            if file_id=="all":
                all_invalid_files=FileInfo.objects.all(is_active=0).filter(IsActive=0)
                for file in  all_invalid_files:
                    FileInfoService.clean_build_archive(file.id) 
            else:
                FileInfoService.clean_build_archive(file_id)
        except Exception as ex:
            result=str(ex)
            SimpleLogger.exception(ex)
        return Response(str(result))

class AgentView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = agent_serializer.AgentSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        agent_id =int(self.kwargs['id'])
        return Agent.objects.get(agent_id)
    

    
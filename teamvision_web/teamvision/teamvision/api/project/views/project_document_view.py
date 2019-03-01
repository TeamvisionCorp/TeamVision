#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.http import HttpResponse
from gatesidelib.common.simplelogger import SimpleLogger
from rest_framework import generics,status, response
from teamvision.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from teamvision.api.project.filters import project_filter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.home.models import FileInfo
from teamvision.project import models
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication

from business.project.document_service import DocumentService

class ProjectDocumentView(generics.RetrieveUpdateDestroyAPIView,generics.CreateAPIView):
    """
    /api/project/document/document_id
    update,get,delete document  with document_id
    """
    serializer_class = project_serializer.ProjectDocumentSerializer
    permission_classes=[AllowAny]
    authentication_classes=(CsrfExemptSessionAuthentication,BasicAuthentication)
    

    def get_object(self):
        document_id=self.kwargs.get('document_id',0)
        return models.ProjectDocument.objects.get(document_id)

    def patch(self, request, *args, **kwargs):
        document = self.get_object()
        file = FileInfo.objects.get(document.FileID)
        if file:
            file_name = request.data.get('FileName',None)
            if file_name:
                file.FileName = file_name
                file.save()
        serializer = self.get_serializer(document, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(document, '_prefetched_objects_cache', None):
            document._prefetched_objects_cache = {}
        return response.Response(serializer.data)

    def perform_destroy(self, instance):
        DocumentService.delete_document(instance.id,self.request.user,)

class ProjectDocumentListView(generics.ListCreateAPIView):
    """
    get:
        /api/project/project_id/documents
        get document list with project_id,
        FilterSet: ['ProjectID']
        FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    post:
        create new issue
    """
    serializer_class = project_serializer.ProjectDocumentSerializer
    permission_classes=[AllowAny]
    authentication_classes=(CsrfExemptSessionAuthentication,BasicAuthentication)
    queryset=models.ProjectDocument.objects.all()
    
    def get_queryset(self):
        parent_id = self.request.GET.get('id',None)
        project_id=self.kwargs.get('project_id',0)
        qs = models.ProjectDocument.objects.all()
        if str(project_id)!="0":
            qs=qs.filter(ProjectID=project_id)
        if parent_id is not None:
            qs = qs.filter(Parent=int(parent_id)).filter(Type=1).filter(ReadOnly=False).order_by('-id')
            return qs
        else:
            return project_filter.ProjectDocumentFilterSet(data=self.request.GET, queryset=qs).filter().order_by('-id')

    def create(self, request, *args, **kwargs):
        document = DocumentService.create_document(request.data, request.user)
        serializer = project_serializer.ProjectDocumentSerializer(instance=document, data=request.data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

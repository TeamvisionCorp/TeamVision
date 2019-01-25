#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.http import HttpResponse
from gatesidelib.common.simplelogger import SimpleLogger
from business.common.file_info_service import FileInfoService
from business.common.redis_service import RedisService
from rest_framework import generics,status, response
from teamvision.api.project.serializer import project_serializer
from rest_framework.permissions import AllowAny
from teamvision.api.project.filters import project_issue_filter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.filters.project_pagination import ProjectPagination
from teamvision.home.models import FileInfo
from teamvision.project import models
from teamvision.project.mongo_models import IssueMongoFile
from teamvision.settings import WEB_HOST
from io import BytesIO
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication

from business.project.issue_service import IssueService

class IssueView(generics.RetrieveUpdateDestroyAPIView,generics.CreateAPIView):
    """
    /api/project/issue/issue_id
    update,get,delete issue  with issue_id
    """
    serializer_class = project_serializer.ProjectIssueSerializer
    permission_classes=[AllowAny]
    authentication_classes=(CsrfExemptSessionAuthentication,BasicAuthentication)
    

    def get_object(self):
        issue_id=self.kwargs.get('issue_id',0)
        return models.ProjectIssue.objects.get(issue_id)


    def create(self, request, *args, **kwargs):
        print(kwargs)
        print(request.data)
        issue_id = kwargs.get('issue_id', 0)
        operation_type = request.data.get('operation',0)
        reslove_result = request.data.get('ResloveResult',1)
        comments = request.data.get('Desc')
        IssueService.update_issue_operation_result(issue_id,operation_type,reslove_result,comments,request.user.id)
        return response.Response(status=status.HTTP_200_OK)

class IssueListView(generics.ListCreateAPIView):
    """
    get:
        /api/project/project_id/version_id/issues
        get issue list with project_id,version_id
        FilterSet: ['Project','Version','Status','Module','Processor','IssueCategory','Solution','Severity','Creator','CreationTime','ClosedTime','ResolvedTime']
        FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    post:
        create new issue
    """
    serializer_class = project_serializer.ProjectIssueSerializer
    permission_classes=[AllowAny]
    authentication_classes=(CsrfExemptSessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssue.objects.all()
    pagination_class = ProjectPagination
    
    def get_queryset(self):
        project_id=self.kwargs.get('project_id',0)
        version_id=self.kwargs.get('version_id',0)
        qs = models.ProjectIssue.objects.all()
        if str(project_id)!="0":
            qs=qs.filter(Project=project_id)
        if str(version_id)!="0":
            qs=qs.filter(Version=version_id)
        return project_issue_filter.IssueFilterSet(data=self.request.GET, queryset=qs).filter().order_by('-id')

    def create(self, request, *args, **kwargs):
        issue = IssueService.create_issue(request.data, request.user)
        serializer = project_serializer.ProjectIssueSerializer(instance=issue, data=request.data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class IssueStatusList(generics.ListAPIView):
    """
    /api/project/issue/status
    获取问题状态列表
    """
    serializer_class = project_serializer.ProjectIssueStatuserializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueStatus.objects.all()

class IssuePriorityList(generics.ListAPIView):
    """
    /api/project/issue/priority
    获取问题优先级列表
    """
    serializer_class = project_serializer.ProjectIssuePrioritySerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssuePriority.objects.all()


class ProjectOSList(generics.ListAPIView):
    """
    /api/project/issue/priority
    获取问题优先级列表
    """
    serializer_class = project_serializer.ProjectOSSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectOS.objects.all()

class IssueSeverityList(generics.ListAPIView):
    """
    /api/project/issue/severities
    获取问题状态列表
    """
    serializer_class = project_serializer.ProjectIssueSeveritySerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueSeverity.objects.all()

class IssueCategoryList(generics.ListAPIView):
    """
    /api/project/issue/categories
    获取问题分类列表
    """
    serializer_class = project_serializer.ProjectIssueCategorySerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueCategory.objects.all()


class IssueResolveResultList(generics.ListAPIView):
    """
    /api/project/issue/resolve_results
    获取问题解决结果列表
    """
    serializer_class = project_serializer.ProjectIssueResolvedResultSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectIssueResolvedResult.objects.all()


class IssueProjectPhraseList(generics.ListAPIView):
    """
    /api/project/issue/resolve_results
    获取问题解决结果列表
    """
    serializer_class = project_serializer.ProjectPhraseSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectPhase.objects.all()


class ProjectModuleList(generics.ListAPIView):
    """
    /api/project/project_id/modules
    获取项目模块列表
    """
    serializer_class = project_serializer.ProjectModuleSerializer
    permission_classes=[AllowAny]
    authentication_classes=(SessionAuthentication,BasicAuthentication)
    queryset=models.ProjectModule.objects.all()
    
    def get_queryset(self):
        project_id=self.kwargs.get('project_id',0)
        qs=super(ProjectModuleList, self).get_queryset()
        if project_id:
            qs=qs.filter(ProjectID=project_id)
        return qs


class ProjectIssueAttachementView(generics.RetrieveUpdateDestroyAPIView):
    """
     post  /api/project/issue/<issue_id>/attachment/<file_id>
    upload issue attachment
    """
    serializer_class = project_serializer.ProjectForTestingSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = ProjectPagination

    def delete(self,request, *args, **kwargs):
        file_id = kwargs.get('file_id')
        issue_id = kwargs.get('issue_id')
        IssueService.delete_attachment(file_id, issue_id)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


    def patch(self,request, *args, **kwargs):
        issue_id = kwargs.get('issue_id')
        attachment_key = request.data.get('uploadList', [])
        file_ids = IssueService.store_cached_file(attachment_key)
        issue = models.ProjectIssue.objects.get(int(issue_id))
        if issue:
            issue.Attachments = issue.Attachments + file_ids
            issue.save()
        return response.Response(status=status.HTTP_202_ACCEPTED)

    def get(self,request,*args, **kwargs):
        result = True
        try:
            file_id = kwargs.get('file_id')
            temp_file = RedisService.get_object(file_id)
            if temp_file:
                result = temp_file
            else:
                result = FileInfoService.get_file(int(file_id),IssueMongoFile)
        except Exception as ex:
            result = str(ex)
            SimpleLogger.exception(ex)
        return HttpResponse(result, content_type="application/octet-stream")

class ProjectIssueAttachementListView(generics.CreateAPIView):
    """
     post  /api/project/issue/attachments
    """
    serializer_class = project_serializer.ProjectForTestingSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    pagination_class = ProjectPagination

    def post(self,request, *args, **kwargs):
        '''

        :param request: /api/project/issue/attachments
        :param args:
        :param kwargs:
        :return:
        '''
        file = request.FILES['file']
        message = IssueService.cache_issue_attachments(file, request.user)
        if message['cache_key'] != "":
            return response.Response(
                {'file_id': message["cache_key"], 'url': WEB_HOST + '/api/project/issue/download_file/' + str(message['cache_key'])})
        else:
            return response.Response(status=status.HTTP_417_EXPECTATION_FAILED)


class ProjectIssueExportView(generics.ListAPIView):
    """
    /api/project/<project_id>/issue/export
    upload fortesing attachment
    """
    serializer_class = project_serializer.ProjectForTestingSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


    def get_queryset(self):
        project_issue = models.ProjectIssue.objects.all()
        issue_list = project_issue_filter.IssueFilterSet(data=self.request.GET, queryset=project_issue).filter()
        return issue_list

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id', 0)
        issue_list = self.get_queryset()
        return_result = HttpResponse(content_type='application/vnd.ms-excel')
        return_result['Content-Disposition'] = 'attachment;filename=' + str(project_id) + '.xls'
        output = BytesIO()
        wb = IssueService.issue_excel_file(issue_list, self.request.user.id)
        wb.save(output)
        output.seek(0)
        return_result.write(output.getvalue())
        return return_result


class IssueActivityList(generics.ListCreateAPIView):
    """
    /api/project/issue/<issue_id>/activities
    获取问题解决结果列表
    """
    serializer_class = project_serializer.IssueActivitySerializer
    permission_classes=[AllowAny]
    authentication_classes=(CsrfExemptSessionAuthentication,BasicAuthentication)



    def get_queryset(self):
        issue_id = int(self.kwargs.get('issue_id',0))
        queryset=models.IssueActivity.objects.issue_activity(issue_id)
        return queryset









    

    
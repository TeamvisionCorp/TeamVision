# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.http import HttpResponse
from gatesidelib.common.simplelogger import SimpleLogger
from rest_framework import generics, status, response
from doraemon.api.project.serializer import project_report_serializer
from rest_framework.permissions import AllowAny
from bson import ObjectId
from doraemon.project import mongo_models
from business.project.report_service import ReportService
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from doraemon.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication


class ProjectBVTReportListView(generics.ListCreateAPIView):
    """
    /api/project/report/bvt
    get bvt report  list  and create new bvt report
    FilterSet: Null
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = project_report_serializer.BVTReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return mongo_models.BVTReport.objects.all()

    def post(self, request, *args, **kwargs):
        response =self.create(request, *args, **kwargs)
        ReportService.send_report(response.data.get('id',None),1,request)
        return response


class ProjectBVTReportView(generics.RetrieveUpdateAPIView):
    """
    /api/project/report/id
    get,update,delete report with report_id
    """
    serializer_class = project_report_serializer.BVTReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        report_id = self.kwargs.get('id')
        return mongo_models.BVTReport.objects.get(id=ObjectId(report_id))


class ProjectTestProgressReportListView(generics.ListCreateAPIView):
    """
    /api/project/report/bvt
    get test progress report  list  and create new test progress report
    FilterSet: Null
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = project_report_serializer.TestProgressReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return mongo_models.TestProgressReport.objects.all()

    def post(self, request, *args, **kwargs):
        response =self.create(request, *args, **kwargs)
        ReportService.send_report(response.data.get('id',None),2,request)
        return response



class FortestingTestProgressReportView(generics.RetrieveAPIView):
    """
    /api/project/fortesting/fortesting_id/report/report_type
    report_type: 1,2,3. 1:bvt,2:testprogress,3:testcomplete
    get lastest report by fortesting id
    """
    serializer_class = project_report_serializer.TestProgressReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        result = None
        fortesting_id = int(self.kwargs.get('fortesting_id'))
        report_type = int(self.kwargs.get('report_type').strip())
        if report_type == 1:
            FortestingTestProgressReportView.serializer_class = project_report_serializer.BVTReportSerializer
            report_list = mongo_models.BVTReport.objects.filter(FortestingID=fortesting_id).filter(
                ReportType=report_type).order_by('-create_time')
        if report_type == 2:
            FortestingTestProgressReportView.serializer_class = project_report_serializer.TestProgressReportSerializer
            report_list = mongo_models.TestProgressReport.objects.filter(FortestingID=fortesting_id).filter(
                ReportType=report_type).order_by('-create_time')
        if report_type == 3:
            FortestingTestProgressReportView.serializer_class = project_report_serializer.TestingCompleteReportSerializer
            report_list = mongo_models.TestingCompleteReport.objects.filter(FortestingID=fortesting_id).filter(
                ReportType=report_type).order_by('-create_time')
        if len(report_list) > 0:
            result = report_list[0]
        return result


class ProjectTestProgressReportView(generics.RetrieveUpdateAPIView):
    """
    /api/project/fortesting/fortesting_id/report/testprogress
    get,update,delete report with report_id
    """
    serializer_class = project_report_serializer.TestProgressReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        report_id = self.kwargs.get('id')
        return mongo_models.TestProgressReport.objects.get(id=ObjectId(report_id))


class ProjectTestCompleteReportListView(generics.ListCreateAPIView):
    """
    /api/project/report/bvt
    get test progress report  list  and create new test progress report
    FilterSet: Null
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = project_report_serializer.TestingCompleteReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return mongo_models.TestingCompleteReport.objects.all()

    def post(self, request, *args, **kwargs):
        response =self.create(request, *args, **kwargs)
        ReportService.send_report(response.data.get('id',None),3,request)
        return response


class ProjectTestCompleteReportView(generics.RetrieveUpdateAPIView):
    """
    /api/project/report/id
    get,update,delete report with report_id
    """
    serializer_class = project_report_serializer.TestingCompleteReportSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        report_id = self.kwargs.get('id')
        return mongo_models.TestingCompleteReport.objects.get(id=ObjectId(report_id))

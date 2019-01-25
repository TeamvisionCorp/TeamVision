# coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.project.pagefactory.project_pageworker import ProjectPageWorker
from teamvision.project.pagefactory.project_template_path import ProjectEmailReportPath
from teamvision.project.mongo_models import BVTReport, TestProgressReport, TestingCompleteReport
from bson import ObjectId


class ProjectEmailReportPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self, request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)

    def get_bvt_report(self, report_id):
        bvt_report = BVTReport.objects.get(id=ObjectId(report_id))
        feature_container_height = len(bvt_report.FeatureProgress.Feature)*35+100
        page_fields = {'report': bvt_report,'feature_container_height':feature_container_height}
        return self.get_webpart(page_fields, ProjectEmailReportPath.email_bvt_report)

    def get_testprogress_report(self, report_id):
        testprogress_report = TestProgressReport.objects.get(id=ObjectId(report_id))
        feature_container_height = len(testprogress_report.FeatureProgress.Feature)*35+100
        page_fields = {'report': testprogress_report,'feature_container_height':feature_container_height}
        return self.get_webpart(page_fields, ProjectEmailReportPath.email_testprogress_report)

    def get_testcomplete_report(self, report_id):
        testcomplete_report = TestingCompleteReport.objects.get(id=ObjectId(report_id))
        feature_container_height = len(testcomplete_report.FeatureProgress.Feature)*35+100
        page_fields = {'report': testcomplete_report,'feature_container_height':feature_container_height}
        return self.get_webpart(page_fields, ProjectEmailReportPath.email_testcomplete_report)

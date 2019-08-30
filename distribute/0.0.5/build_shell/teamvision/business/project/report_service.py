# coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from teamvision.project.mongo_models import  BVTReport,TestProgressReport,TestingCompleteReport
from gatesidelib.common.simplelogger import SimpleLogger
from gatesidelib.datetimehelper import DateTimeHelper
from business.common.system_config_service import SystemConfigService
from business.auth_user.user_service import UserService
from business.business_service import BusinessService
from teamvision.project.pagefactory.project_emailreport_pageworker import ProjectEmailReportPageWorker
from bson import  ObjectId


class ReportService(BusinessService):
    '''
    classdocs
    '''

    @staticmethod
    def send_report(report_id, report_type, request):
        page_worker = ProjectEmailReportPageWorker(request)
        try:
            if report_type == 1:
                bvt_report = BVTReport.objects.get(id=ObjectId(report_id))
                email_content = page_worker.get_bvt_report(report_id)
                email_list = ReportService.get_email_list(bvt_report)
                ReportService.send_notification_email(email_list,bvt_report.Topic,email_content)

            if report_type == 2:
                testprogress_report = TestProgressReport.objects.get(id=ObjectId(report_id))
                email_content = page_worker.get_testprogress_report(report_id)
                email_list = ReportService.get_email_list(testprogress_report)
                ReportService.send_notification_email(email_list,testprogress_report.Topic,email_content)

            if report_type == 3:
                testcomplete_report = TestingCompleteReport.objects.get(id=ObjectId(report_id))
                email_content = page_worker.get_testcomplete_report(report_id)
                email_list = ReportService.get_email_list(testcomplete_report)
                ReportService.send_notification_email(email_list,testcomplete_report.Topic,email_content)

        except Exception as ex:
            SimpleLogger.exception(ex)

    @staticmethod
    def send_notification_email(email_list, email_topic,email_content):
        ReportService.send_email(None,email_list,email_content,email_topic)

    @staticmethod
    def get_email_list(report):
        email_list = list()
        if len(report.Recipients):
            for recipient in report.Recipients:
                user = UserService.get_user(recipient)
                if user and user.email not in email_list:
                    email_list.append(user.email)
        if report.CCList:
            cc_email_recipients = report.CCList.split(',')
            for recipient in cc_email_recipients:
                if recipient.strip() not in email_list:
                    email_list.append(recipient.strip())
        ReportService.get_default_email_list(email_list)
        return email_list



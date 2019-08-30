#coding=utf-8
'''
Created on 2015-2-4

@author: zhangtiande
'''
from dataaccess.testjob.dal_testjob import DAL_TestJob
from dataaccess.testjob.dal_testsubmition import DAL_TestSubmition
from dataaccess.productquality.dal_bugreport import DAL_BugReport
from gatesidelib.datetimehelper import DateTimeHelper
from gatesidelib.common.simplelogger import SimpleLogger
import datetime

class BugReportService(object):
    '''
    business service for bug report
    '''
    
    @staticmethod
    def get_perday_bugcounts_data(submitionid):
        SimpleLogger.logger.info("business for submitionid"+submitionid)
        opened_bugcounts_results=BugReportService.get_perday_openedbugcounts_data(submitionid)
        dates=opened_bugcounts_results[0]
        openedbugcounts=opened_bugcounts_results[1]
        resolvedbugcounts=BugReportService.get_perday_resolvedbugcounts_data(submitionid)[1]
        closedbugcounts=BugReportService.get_perday_closedbugcounts_data(submitionid)[1]
        return str(dates)+";"+str(openedbugcounts)+";"+str(resolvedbugcounts)+";"+str(closedbugcounts)
    
    @staticmethod
    def get_perday_openedbugcounts_data(submitionid):
        bugcounts=list()
        result=list()
        query_info=BugReportService.get_query_info(submitionid)
        openedresult=DAL_BugReport.get_opened_bugcounts_perday(str(query_info[0]),str(query_info[1]),query_info[2])
        result_dict=BugReportService.get_chartdata(openedresult,str(query_info[0]),str(query_info[1]))
        datelist=DateTimeHelper.generate_datelist(str(query_info[0]),str(query_info[1]))
        for date in datelist:
            bugcounts.append(result_dict[str(date)])
        result.append(datelist)
        result.append(bugcounts)
        return result
    
    @staticmethod
    def get_perday_resolvedbugcounts_data(submitionid):
        bugcounts=list()
        result=list()
        query_info=BugReportService.get_query_info(submitionid)
        openedresult=DAL_BugReport.get_resolved_bugcounts_perday(str(query_info[0]),str(query_info[1]),query_info[2])
        result_dict=BugReportService.get_chartdata(openedresult,str(query_info[0]),str(query_info[1]))
        datelist=DateTimeHelper.generate_datelist(str(query_info[0]),str(query_info[1]))
        for date in datelist:
            bugcounts.append(result_dict[str(date)])
        result.append(datelist)
        result.append(bugcounts)
        return result
    
    @staticmethod
    def get_perday_closedbugcounts_data(submitionid):
        bugcounts=list()
        result=list()
        query_info=BugReportService.get_query_info(submitionid)
        openedresult=DAL_BugReport.get_closed_bugcounts_perday(str(query_info[0]),str(query_info[1]),query_info[2])
        result_dict=BugReportService.get_chartdata(openedresult,str(query_info[0]),str(query_info[1]))
        datelist=DateTimeHelper.generate_datelist(str(query_info[0]),str(query_info[1]))
        for date in datelist:
            bugcounts.append(result_dict[str(date)])
        result.append(datelist)
        result.append(bugcounts)
        return result
    
    
    @staticmethod
    def get_all_openedbugcounts_data(submitionid):
        bugcounts=list()
        result=list()
        query_info=BugReportService.get_query_info(submitionid)
        openedresult=DAL_BugReport.get_opened_bugcounts_perday(str(query_info[0]),str(query_info[1]),query_info[2])
        result_dict=BugReportService.get_chartdata(openedresult,str(query_info[0]),str(query_info[1]))
        datelist=DateTimeHelper.generate_datelist(str(query_info[0]),str(query_info[1]))
        i=0
        for date in datelist:
            if len(bugcounts):
                all_opendbugcounts=bugcounts[i]+int(result_dict[str(date)])
                i=i+1
            else:
                all_opendbugcounts=int(result_dict[str(date)])
                i=0
            bugcounts.append(all_opendbugcounts)
            all_opendbugcounts=0 
        result.append(datelist)
        result.append(bugcounts)
        return result
    
    @staticmethod
    def get_all_resolvedbugcounts_data(submitionid):
        bugcounts=list()
        result=list()
        query_info=BugReportService.get_query_info(submitionid)
        openedresult=DAL_BugReport.get_resolved_bugcounts_perday(str(query_info[0]),str(query_info[1]),query_info[2])
        result_dict=BugReportService.get_chartdata(openedresult,str(query_info[0]),str(query_info[1]))
        datelist=DateTimeHelper.generate_datelist(str(query_info[0]),str(query_info[1]))
        i=0
        for date in datelist:
            if len(bugcounts):
                all_opendbugcounts=bugcounts[i]+int(result_dict[str(date)])
                i=i+1
            else:
                all_opendbugcounts=int(result_dict[str(date)])
                i=0
            bugcounts.append(all_opendbugcounts)
            all_opendbugcounts=0
        result.append(datelist)
        result.append(bugcounts)
        return result
    
    @staticmethod
    def get_all_closedbugcounts_data(submitionid):
        bugcounts=list()
        result=list()
        query_info=BugReportService.get_query_info(submitionid)
        openedresult=DAL_BugReport.get_closed_bugcounts_perday(str(query_info[0]),str(query_info[1]),query_info[2])
        result_dict=BugReportService.get_chartdata(openedresult,str(query_info[0]),str(query_info[1]))
        datelist=DateTimeHelper.generate_datelist(str(query_info[0]),str(query_info[1]))
        i=0
        for date in datelist:
            if len(bugcounts):
                all_opendbugcounts=bugcounts[i]+int(result_dict[str(date)])
                i=i+1
            else:
                all_opendbugcounts=int(result_dict[str(date)])
                i=0
            bugcounts.append(all_opendbugcounts)
            all_opendbugcounts=0 
        result.append(datelist)
        result.append(bugcounts)
        return result
        
    
    @staticmethod
    def get_all_bugcounts_data(submitionid):
        allopened_bugcounts_results=BugReportService.get_all_openedbugcounts_data(submitionid)
        dates=allopened_bugcounts_results[0]
        all_openedbugcounts=allopened_bugcounts_results[1]
        all_resolvedbugcounts=BugReportService.get_all_resolvedbugcounts_data(submitionid)[1]
        all_closedbugcounts=BugReportService.get_all_closedbugcounts_data(submitionid)[1]
        return str(dates)+";"+str(all_openedbugcounts)+";"+str(all_resolvedbugcounts)+";"+str(all_closedbugcounts)
    
    @staticmethod
    def get_query_info(submitionid):
        query_info=list()
        testjobs=DAL_TestJob.getjobsbysubmitionid(submitionid)
        today=str(datetime.date.today())
        if len(testjobs):
            testjob=testjobs[0]
            query_info.append(testjob.TJStartTime)
            if testjob.TJFinishedTime:
                tempDate=str(DateTimeHelper.add_day(str(testjob.TJFinishedTime),1))[0:10]
                query_info.append(tempDate)
            elif int(testjob.TJProgress)==100:
                tempDate=str(DateTimeHelper.add_day(str(testjob.TJEndTime),1))[0:10]
                query_info.append(tempDate)
            else:
                query_info.append(str(datetime.date.today()))
                query_info[1]=str(DateTimeHelper.add_day(query_info[1],1))[0:10]
        else:
            query_info.append(str(datetime.date.today()))
            query_info.append(str(DateTimeHelper.add_day(today,1))[0:10])
        testsubmition=DAL_TestSubmition.gettestsubmition(submitionid)
        bugfree_mapping_item=DAL_BugReport.get_bugfree_module(testsubmition.TPSProductName,testsubmition.TPSPlatform)
        query_info.append(bugfree_mapping_item.BugfreeProjectID)
        return query_info
    
    @staticmethod
    def get_chartdata(queryset,startdate,enddate):
        result=dict()
        datelist=DateTimeHelper.generate_datelist(startdate,enddate)
        for date in datelist:
            result[str(date)]=0
        for item in queryset:
            result[str(item[0])]=item[1]
        return result
        
    @staticmethod
    def get_allbugcounts(submitionid):
        query_info=BugReportService.get_query_info(submitionid)
        openedresult=DAL_BugReport.get_opened_bugcounts_all(str(query_info[0]),str(query_info[1]),query_info[2])
        if len(openedresult):
            return int(openedresult[0][0])
        else:
            return 0
            
                        
        
        
    
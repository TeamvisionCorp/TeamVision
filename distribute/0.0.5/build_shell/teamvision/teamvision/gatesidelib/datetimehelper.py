#coding=utf-8
'''
Created on 2014-10-9

@author: zhangtiande
'''
import time
import datetime

class DateTimeHelper(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_timestamp(start_time,time_format):
        return time.mktime(time.strptime(start_time,time_format))*1000
        
        
    
    @staticmethod
    def get_time_to_now(start_time,time_format):
        '''
            diff for start_time and now
            return value: seconds
        '''
        now=datetime.datetime.now()
        start_time=datetime.datetime.strptime(start_time,time_format)  
        return (now-start_time).total_seconds()
    
    
    
    @staticmethod
    def getcnow():
        now=time.time()
        timeArray = time.localtime(now)
        local_date_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return local_date_time
    
    @staticmethod
    def get_local_now(interval):
        return datetime.datetime.now()+datetime.timedelta(hours=interval)
    
    @staticmethod
    def generate_datelist(start,end):
        result=list()
        startdatetime=time.strptime(start,'%Y-%m-%d')
        startdate=datetime.datetime(*startdatetime[:3])
        enddate=datetime.datetime(*time.strptime(end,'%Y-%m-%d')[:3])
        while startdate<enddate:
            result.append(str(startdate)[:10])
            startdate=startdate+datetime.timedelta(1)
        return result
    
    @staticmethod
    def add_day(sourcedate,days):
        '''
        sourcedate: '2015-02-03'
        days: 3
        '''
        targetdatetime=time.strptime(sourcedate,'%Y-%m-%d')
        targetdate=datetime.datetime(*targetdatetime[:3])+datetime.timedelta(days)
        return targetdate
    
    @staticmethod
    def how_long_ago(seconds):
        if DateTimeHelper.seconds_to_year(seconds):
            return str(DateTimeHelper.seconds_to_year(seconds))+"年前"
        
        if DateTimeHelper.seconds_to_month(seconds):
            return str(DateTimeHelper.seconds_to_month(seconds))+"月前"
        if DateTimeHelper.seconds_to_day(seconds):
            return str(DateTimeHelper.seconds_to_day(seconds))+"天前"
        
        if DateTimeHelper.seconds_to_hour(seconds):
            return str(DateTimeHelper.seconds_to_hour(seconds))+"小时前"
        
        if DateTimeHelper.seconds_to_minitue(seconds):
            return str(DateTimeHelper.seconds_to_minitue(seconds))+"分钟前"
        return str(seconds)+"秒前"
        
        
    
    @staticmethod
    def seconds_to_year(seconds):
        return int(seconds/60/60/24/365)
    
    @staticmethod
    def seconds_to_month(seconds):
        return int(seconds/60/60/24/30)
    
    @staticmethod
    def seconds_to_day(seconds):
        return int(seconds/60/60/24)
    
    @staticmethod
    def seconds_to_hour(seconds):
        return int(seconds/60/60)
    
    @staticmethod
    def seconds_to_minitue(seconds):
        return int(seconds/60)
    
    
    
    
    
        
        
        
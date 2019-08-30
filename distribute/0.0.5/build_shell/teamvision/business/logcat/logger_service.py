#coding=utf-8
'''
Created on 2017年4月20日

@author: zhangtiande
'''

from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from teamvision.logcat.mongo_models import BusinessLog
from business.common.redis_service import RedisService
from teamvision.logcat.models import Logger
from builtins import staticmethod
from gatesidelib.common.simplelogger import SimpleLogger

class LoggerService(object):
    '''
    classdocs
    '''


    @staticmethod
    def publicsh_message(facility,message):
        message_data = RedisMessage(message)  # create a welcome message to be sent to everybody
        RedisPublisher(facility=facility, broadcast=True).publish_message(message_data)
    
    @staticmethod
    def get_log_from_request(request):
        app_id=request.data.get('appId')
        user_id=request.data.get('userId',"--")
        event_id=request.data.get('eventId')
        channel=request.data.get("channel")
        model=request.data.get("model")
        os=request.data.get("os")
        data=request.data.get("data")
        deviceId=request.data.get("deviceId")
        appVersion=request.data.get("appVersion")
        result="*****************"+"<br/>"
        result=result+"EventID: "+str(event_id)+"  AppId: "+str(app_id)+"  UserId: "+str(user_id)
        result=result+" AppVersion: "+str(appVersion)+"  DeviceID: "+str(deviceId)+" </br>"
        result=result+"Data: "+data+"<br/>"
        return result
    
    @staticmethod
    def delete_logger(logger_id):
        dm_logger=Logger.objects.get(int(logger_id))
        dm_logger.IsActive=0
        dm_logger.save();
        
    
    @staticmethod
    def get_more_logs(device_id,start_index,end_index):
        result="False"
        bslogs=LoggerService.get_bslogs_by_deviceid(device_id)[start_index:end_index]
        if len(bslogs)==0:
            result="False"
        else:
            result="<br/>"
        for log in bslogs:
            result=result+"*****************"+"<br/>"
            result=result+"EventID: "+str(log.eventId)+"  AppId: "+str(log.appId)+"  UserId: "+str(log.userId)
            result=result+" AppVersion: "+str(log.appVersion)+"  DeviceID: "+str(log.deviceId)+" </br>"
            result=result+"Data: "+log.data+"<br/>"
        return result
    
    
    @staticmethod
    def get_bslogs_by_deviceid(device_id):
        result=list()
        try:
            result=BusinessLog.objects.all().filter(deviceId=device_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
        
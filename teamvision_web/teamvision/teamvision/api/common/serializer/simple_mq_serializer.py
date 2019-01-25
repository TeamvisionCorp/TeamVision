#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''
from teamvision.api.common.models import MessageQueue
from business.common.redis_service import RedisService
from rest_framework import serializers
from multiprocessing.connection import deliver_challenge


class SimpleMQSerializer(serializers.Serializer):
    channel=serializers.CharField()
    message=serializers.CharField()
    delivered_count=serializers.IntegerField(required=False)
    
    def save(self):
        channel = self.validated_data['channel']
        message = self.validated_data['message']
        delivered_count=RedisService.publish_message(channel, message)
        RedisService.websocket_publish_message(channel,message)
        self.validated_data['delivered_count']=delivered_count
        
        
        
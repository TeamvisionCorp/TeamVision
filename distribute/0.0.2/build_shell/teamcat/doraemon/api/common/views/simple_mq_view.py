#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from rest_framework import generics
from doraemon.api.common.serializer import simple_mq_serializer
from rest_framework.permissions import AllowAny


class SimpleMQView(generics.CreateAPIView):
    """
    path: /api/common/simple_mq
    args: channel:消息队列渠道名称@String,message:消息体@String
    """
    
    serializer_class = simple_mq_serializer.SimpleMQSerializer
    permission_classes=[AllowAny]
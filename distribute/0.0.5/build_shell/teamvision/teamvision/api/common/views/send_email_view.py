#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from rest_framework import generics
from teamvision.api.common.serializer import email_sender_serializer
from rest_framework.permissions import AllowAny


class EmailSendView(generics.CreateAPIView):
    """
    path: /api/common/send_email
    args: subject:邮件名称@String,content:消息体@String,reciver_list: 收件人邮箱列表@List
    """
    
    serializer_class = email_sender_serializer.EmailSenderSerializer
    permission_classes=[AllowAny]
#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from business.common.emailservice import EmailService


class EmailSenderSerializer(serializers.Serializer):
    subject=serializers.CharField()
    content=serializers.CharField()
    reciver_list = serializers.ListField(child=serializers.CharField(max_length=100))
    
    def save(self):
        subject = self.validated_data['subject']
        content = self.validated_data['content']
        reciver_list = self.validated_data['reciver_list']
        EmailService.sendemail(None,reciver_list,content,subject)

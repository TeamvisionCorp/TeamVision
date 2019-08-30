#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from rest_framework import generics
from django.http import HttpResponse
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.api.common.serializer import dic_config_serializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from gatesidelib.qr_code_helper import QRCodeHelper

class QRCodeView(generics.RetrieveAPIView):
    """
    /api/common/toolkit/qrcode?content=xxxx
    """
    # serializer_class = dic_config_serializer.DicConfigSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)

    def get(self, request, *args, **kwargs):
        try:
            content = request.GET.get('content', "")
            code_image = QRCodeHelper.save_qr_code_stream(content)
            response = HttpResponse(code_image, content_type="image/png")
        except Exception as ex:
            SimpleLogger.exception(ex)
        return response

        return qs

    
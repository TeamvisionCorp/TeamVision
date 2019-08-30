#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.contrib.auth.models import User
from django.http import HttpResponse
from gatesidelib.common.simplelogger import SimpleLogger
from rest_framework import generics,response,status
from teamvision.settings import WEB_HOST
from business.ucenter.account_service import AccountService
from rest_framework.permissions import AllowAny
from teamvision.user_center.mongo_models import UCenterMongoFile
from teamvision.project.mongo_models import TempFileMongoFile
from teamvision.api.ucenter.serializer.user_serializer import UserSerializer

from rest_framework.authentication import BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication


class UCenterProfilesAvatarView(generics.RetrieveUpdateDestroyAPIView):
    """
     post  /api/project/issue/<issue_id>/attachment/<file_id>
    upload issue attachment
    """
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def delete(self,request, *args, **kwargs):
        file_id = kwargs.get('file_id',None)
        if file_id is not None:
            file_list = file_id.split(",")
            for id in file_list:
                AccountService.delete_tempfile(id)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


    def patch(self,request, *args, **kwargs):
        attachment_key = request.data.get('uploadList', [])
        AccountService.update_avatar(request.user,attachment_key)
        return response.Response(status=status.HTTP_202_ACCEPTED)

    def get(self,request,*args, **kwargs):
        result = None
        try:
            file_id = kwargs.get('file_id')
            if file_id.isnumeric():
                result = AccountService.download_attachment(file_id,UCenterMongoFile)
            else:
                result =TempFileMongoFile.objects.get(file_id)
        except Exception as ex:
            result = str(ex)
            SimpleLogger.exception(ex)
        return HttpResponse(result, content_type="application/octet-stream")

    def get_serializer_class(self):
        return UserSerializer

class UCenterUploadView(generics.CreateAPIView):
    """
     post  /api/ucenter/attachment/upload
    """
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_serializer_class(self):
        return UserSerializer


    def post(self,request, *args, **kwargs):
        '''
        :param request: /api/ucenter/attachment/upload
        :param args:
        :param kwargs:
        :return:
        '''
        file = request.FILES['file']
        message = AccountService.cache_issue_attachments(file, request.user)
        if message['cache_key'] != "":
            return response.Response(
                {'file_id': message["cache_key"], 'url': WEB_HOST + '/api/ucenter/profiles/download_file/' + str(message['cache_key'])})
        else:
            return response.Response(message,status=status.HTTP_417_EXPECTATION_FAILED)

    
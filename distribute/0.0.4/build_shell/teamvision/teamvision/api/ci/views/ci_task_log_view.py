# coding=utf-8
'''
Created on 2018-7-3

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CITask
from rest_framework.response import Response
from business.ci.ci_task_service import CITaskService
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from gatesidelib.common.simplelogger import SimpleLogger
from business.common.redis_service import RedisService




class CITaskLogView(generics.RetrieveAPIView):
    """
    path:/api/ci/task_basic/<id>/<operation>?BuildParameter/TaskUUID
    id:taskid
    operation:start,stop,prelog
    BuildParameter: 可选,
    TaskUUID: operation 为stop时必选
    """
    serializer_class = ci_serializer.CITaskSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


    def get_object(self):
        pass

    def get(self,request, *args, **kwargs):
        result = ''
        task_queueid = self.kwargs.get('tq_id',None)
        try:
            if task_queueid:
                result = RedisService.get_value("ci_build_log"+str(task_queueid))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return Response({'PreLog':result})
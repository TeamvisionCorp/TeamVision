# coding=utf-8
# coding=utf-8
'''
Created on 2014-8-5

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CITaskHistory
from teamvision.api.ci.filters.ci_task_history_filter import CITaskHistoryFilterSet
from business.ci.ci_task_history_service import CITaskHistoryService
from rest_framework.response import Response
from teamvision.api.ci.filters.ci_pagination import CIPagination
from teamvision.api.ci.render.ci_task_history_render import CITaskHistoryListRenderer
from gatesidelib.common.simplelogger import SimpleLogger
import threading


class CITaskHistoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.CITaskHistorySerializer
    permission_classes = [AllowAny]

    def get_object(self):
        history_id = int(self.kwargs['id'])
        return CITaskHistory.objects.get(history_id)

    def patch(self, request, *args, **kwargs):
        change_log = request.data.get("ChangeLog")
        tags = request.data.get("Tags")
        if change_log:
            request.data["ChangeLog"] = str(CITaskHistoryService.save_change_log(change_log))
        if tags:
            self.archive_package(tags, kwargs['id'])
        return self.partial_update(request)

    def archive_package(self, tags, history_id):
        if 13 in eval(tags):
            worker = threading.Thread(target=CITaskHistoryService.archive_release_package, args=(history_id,))
            worker.start()
        elif 14 in eval(tags):
            worker = threading.Thread(target=CITaskHistoryService.archive_release_package, args=(history_id,))
            worker.start()


class CITaskHistoryChangeLogView(generics.RetrieveAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = None
    permission_classes = [AllowAny]

    #     def get_object(self):
    #         history_id =int(self.kwargs['id'])
    #         return CITaskHistory.objects.get(history_id)

    def get(self, request, *args, **kwargs):
        result = ""
        history_id = int(self.kwargs['history_id'])
        history = CITaskHistory.objects.get(history_id)
        if history.ChangeLog:
            result = CITaskHistoryService.get_change_log(history.ChangeLog)
            result.pop('_id')
        return Response(str(result))


class CITaskHistoryListView(generics.ListCreateAPIView):
    """
    /api/task/(<task_id>)/task_histories/
    get all ci task list with project_id and create new ci task
    FilterSet: id,TaskQueueID
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = ci_serializer.CITaskHistorySerializer
    permission_classes = [AllowAny]
    pagination_class = CIPagination
    renderer_classes = [CITaskHistoryListRenderer]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        qs = CITaskHistory.objects.all().filter(CITaskID=task_id).order_by('-id')
        return CITaskHistoryFilterSet(data=self.request.GET, queryset=qs).filter()


class CITaskCleanHistoryView(generics.RetrieveAPIView):
    serializer_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        result = "ok"
        try:
            history_id = self.kwargs['history_id']
            CITaskHistoryService.clean_build_history(history_id)
        except Exception as ex:
            result = str(ex)
            SimpleLogger.exception(ex)
        return Response(str(result))

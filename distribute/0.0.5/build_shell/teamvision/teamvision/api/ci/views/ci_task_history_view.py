# coding=utf-8
# coding=utf-8
'''
Created on 2014-8-5

@author: zhangtiande
'''
from rest_framework import generics,response
from django.http import HttpResponse
from teamvision.api.ci.serializer import ci_taskhistory_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CITaskHistory,CITaskStageHistory,CITaskStepOutput
from teamvision.api.ci.filters.ci_task_history_filter import CITaskHistoryFilterSet,CITaskStageHistoryFilterSet
from business.ci.ci_task_history_service import CITaskHistoryService
from business.ci.ci_testing_history_service import CITestingHistoryService
from business.ci.ci_task_config_service import  CITaskConfigService
from rest_framework.response import Response
from teamvision.api.ci.filters.ci_pagination import CIPagination
from teamvision.api.ci.render.ci_task_history_render import CITaskHistoryListRenderer
from gatesidelib.common.simplelogger import SimpleLogger
from rest_framework.authentication import  BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from business.common.redis_service import RedisService
import threading
from io import BytesIO


class CITaskHistoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_taskhistory_serializer.CITaskHistorySerializer
    permission_classes = [AllowAny]

    def get_object(self):
        history_id = int(self.kwargs['id'])
        return CITaskHistory.objects.get(history_id)

    def patch(self, request, *args, **kwargs):
        change_log = request.data.get("ChangeLog")
        tags = request.data.get("Tags")
        if change_log:
            request.data["ChangeLog"] = str(CITaskHistoryService.save_change_log(change_log))
        # if tags:
        #     self.archive_package(tags, kwargs['id'])
        return self.partial_update(request)

    def delete(self, request, *args, **kwargs):
        result = "ok"
        try:
            history_id = self.kwargs['history_id']
            CITaskHistoryService.clean_build_history(history_id)
        except Exception as ex:
            result = str(ex)
            SimpleLogger.exception(ex)
        return Response(str(result))




    # def archive_package(self, tags, history_id):
    #     if 13 in eval(tags):
    #         worker = threading.Thread(target=CITaskHistoryService.archive_release_package, args=(history_id,))
    #         worker.start()
    #     elif 14 in eval(tags):
    #         worker = threading.Thread(target=CITaskHistoryService.archive_release_package, args=(history_id,))
    #         worker.start()


class CITaskHistoryChangeLogView(generics.RetrieveAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = None
    permission_classes = [AllowAny]

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
    /api/ci/task/(<task_id>)/task_histories/
    get all ci task list with project_id and create new ci task
    FilterSet: id,TaskQueueID
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = ci_taskhistory_serializer.CITaskHistorySerializer
    permission_classes = [AllowAny]
    pagination_class = CIPagination
    renderer_classes = [CITaskHistoryListRenderer]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        qs = CITaskHistory.objects.all().filter(CITaskID=task_id).order_by('-id')
        return CITaskHistoryFilterSet(data=self.request.GET, queryset=qs).filter()


class CITaskStageHistoryListView(generics.ListCreateAPIView):
    """
    /api/ci/task_history/(<history_id>)/stage_histories/
    FilterSet: id,TQUUID
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = ci_taskhistory_serializer.CITaskStageHistorySerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        history_id = self.kwargs['history_id']
        qs = CITaskStageHistory.objects.get_sthistory_bythistory_id(history_id).order_by('id')
        return CITaskStageHistoryFilterSet(data=self.request.GET, queryset=qs).filter()


class CITaskStageHistoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/ci/task/stage_history/<stage_history_id>
    get
    put
    patch
    delete
    FilterSet: id,TQUUID
    FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = ci_taskhistory_serializer.CITaskStageHistorySerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        history_id = self.kwargs['stage_history_id']
        stage_history = CITaskStageHistory.objects.get(int(history_id))
        return stage_history

class CITaskStageHistoryLogView(generics.RetrieveAPIView):
    """
        /api/ci/task/stage_history/<stage_history_id>/logs
        get
        """
    serializer_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        result = list()
        stage_history_id = self.kwargs['stage_history_id']
        step_outputs = CITaskStepOutput.objects.filter(StageHistoryID=int(stage_history_id)).filter(ProductType=1).order_by('id')
        stage_history = CITaskStageHistory.objects.get(int(stage_history_id))
        task_history_id =0
        for output in step_outputs:
            task_history_id = output.TaskHistoryID
            if output.ProductID:
                temp_output = CITaskHistoryService.get_log_content(output,False)
                result.append(temp_output)
        if task_history_id !=0 and self.is_last_stage(stage_history):
            last_output = self.get_finished_step_log(task_history_id)
            if last_output is not None:
                result.append(last_output)
        return Response(result)


    def get_finished_step_log(self,task_history_id):
        result = None
        step_outputs = CITaskStepOutput.objects.filter(TaskHistoryID=int(task_history_id)).filter(StageHistoryID=0).filter(ProductType=1)
        if len(step_outputs)>0:
            if step_outputs[0].ProductID:
                contents = CITaskHistoryService.get_big_build_log(step_outputs[0].ProductID)
                temp_output = dict()
                temp_output["id"] = step_outputs[0].id
                temp_output["step_name"] = "完成"
                c = contents.read()
                log_content  = c.decode('utf-8')
                log_content = CITaskHistoryService.format_build_log(log_content)
                temp_output["log_content"] = log_content
                temp_output["show_content"] = True
                result = temp_output
        return result

    def is_last_stage(self,obj):
        result = False
        task_stages = CITaskConfigService.task_stage_list(obj.TaskID)
        try:
            stage_length = len(task_stages)
            last_stage = task_stages[stage_length-1]
            if str(last_stage.id)  == obj.StageID:
                result = True
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result





class CITaskStepLogView(generics.RetrieveAPIView,generics.CreateAPIView):
    """
        /api/ci/task/output/<output_id>/log
        get
        /api/ci/task/output/log/create
        post
        """
    serializer_class = ci_taskhistory_serializer.CITaskOutputSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        result = None
        output_id = int(self.kwargs.get("output_id",0))
        output = CITaskStepOutput.objects.get(output_id)
        if output.ProductID:
            temp_output = CITaskHistoryService.get_log_content(output,True)
            result = temp_output
        return Response(result)

    def post(self, request, *args, **kwargs):
        result = "OK"
        try:
            message = request.data.get("msg", '')
            tq_id = request.data.get("tq_id")
            message_intime = message
            RedisService.append_value("ci_build_log" + str(tq_id), message_intime, 7200)
            welcome = RedisMessage(message_intime)  # create a welcome message to be sent to everybody
            RedisPublisher(facility=str(tq_id), broadcast=True).publish_message(welcome)
        except Exception as ex:
            SimpleLogger.exception(ex)
            result = str(ex)
        return Response(result)


class CITaskStepTestResultExportView(generics.RetrieveAPIView):
    """
        /api/ci/task/output/export_case_result/<result_id>
        get
    """
    serializer_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        test_resultid = self.kwargs.get('result_id')
        response_result = HttpResponse(content_type='application/vnd.ms-excel')
        response_result['Content-Disposition'] = 'attachment;filename={0}.xls'.format(str(test_resultid))
        output = BytesIO()
        wb = CITestingHistoryService.case_result_excel_file(int(test_resultid))
        wb.save(output)
        output.seek(0)
        response_result.write(output.getvalue())
        return response_result




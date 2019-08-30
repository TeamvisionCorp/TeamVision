#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics,status
from django.http import HttpResponse,StreamingHttpResponse
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CITask,CITaskHistory,CITaskStageHistory,CITaskStepOutput
from teamvision.ci import mongo_models
from teamvision.home.models import FileInfo
from business.ci.ci_task_config_service import CITaskConfigService
from rest_framework.response import Response
from teamvision.api.ci.serializer import ci_step_serializer
from teamvision.api.ci.serializer import ci_taskhistory_serializer
from business.ci.ci_task_parameter_service import  CITaskParameterService
from business.ci.ci_task_history_service import CITaskHistoryService
from business.ci.ci_task_service import CITaskService
from business.ci.ci_task_queue_service import CITQService
from business.common.file_info_service import FileInfoService
from teamvision.api.ci.filters.ci_task_history_filter import CITaskStepOutPutFilterSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from teamvision.settings import WEB_HOST
from gatesidelib.common.simplelogger import SimpleLogger
from gatesidelib.qr_code_helper import QRCodeHelper



class CITaskStageView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
         path:/api/ci/task/task_stage/<stage_id>
    put:
         path:/api/ci/task/task_stage/<stage_id>
    delete:
         path:/api/ci/task/task_stage/<stage_id>
    """
    serializer_class = ci_serializer.CITaskStageSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        stage_id = self.kwargs['stage_id']
        return CITaskConfigService.task_stage(stage_id)

    def delete(self, request, *args, **kwargs):
        stage_id = self.kwargs['stage_id']
        CITaskConfigService.delete_steps(stage_id)
        stage = CITaskConfigService.task_stage(stage_id)
        parameter_groups = CITaskParameterService.task_parameter_list(stage.task_id)
        for group in parameter_groups:
            CITaskParameterService.save_step_settings(str(group.id))
        return self.destroy(request, *args, **kwargs)

class CITaskStageCreateView(generics.CreateAPIView):
    """
    post:
         path:/api/ci/task/<task_id>/create_stage
    """
    serializer_class = ci_serializer.CITaskStageSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        task_id = self.kwargs['task_id']
        return CITask.objects.get(int(task_id))


class CITaskStepTempleteView(generics.RetrieveAPIView):
    """
    get:
         path:/api/ci/task/steps
    """
    serializer_class = ci_serializer.CITaskStageSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        result = {}
        result[ci_step_serializer.CITaskSvnStepSerializer().step_id()] = ci_step_serializer.CITaskSvnStepSerializer().to_json()
        result[ci_step_serializer.CITaskGitStepSerializer().step_id()] = ci_step_serializer.CITaskGitStepSerializer().to_json()
        result[ci_step_serializer.CITaskAndroidStepSerializer().step_id()] = ci_step_serializer.CITaskAndroidStepSerializer().to_json()
        result[ci_step_serializer.CITaskIOSStepSerializer().step_id()] = ci_step_serializer.CITaskIOSStepSerializer().to_json()
        result[
            ci_step_serializer.CITaskCommandStepSerializer().step_id()] = ci_step_serializer.CITaskCommandStepSerializer().to_json()
        result[
            ci_step_serializer.CITaskGATAPIStepSerializer().step_id()] = ci_step_serializer.CITaskGATAPIStepSerializer().to_json()
        result[
            ci_step_serializer.CITaskGATUIStepSerializer().step_id()] = ci_step_serializer.CITaskGATUIStepSerializer().to_json()
        result[
            ci_step_serializer.CITaskSSHStepSerializer().step_id()] = ci_step_serializer.CITaskSSHStepSerializer().to_json()

        return Response(result)



class CITaskStepListView(generics.ListCreateAPIView):
    """
    get:
         path:/api/ci/task/task_stage/<stage_id>/steps
    """
    serializer_class = ci_step_serializer.CITaskStepSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


    def get_queryset(self):
        result = list()
        stage_id = self.kwargs.get('stage_id',None)
        if  stage_id is not None:
            result = mongo_models.CITaskStep.objects.all().filter(stage_id=stage_id)
        return result


    def post(self, request, *args, **kwargs):
        stage_id = self.kwargs.get('stage_id', None)
        stage = CITaskConfigService.task_stage(stage_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        parameter_groups = CITaskParameterService.task_parameter_list(stage.task_id)
        for group in parameter_groups:
            CITaskParameterService.save_step_settings(str(group.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CITaskStepView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
         path:/api/ci/task/task_step/<step_id>
    """
    serializer_class = ci_step_serializer.CITaskStepSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


    def get_object(self):
        result = None
        step_id = self.kwargs.get('step_id',None)
        if step_id is not None:
            result = CITaskConfigService.task_step(step_id)
        return result

    def delete(self, request, *args, **kwargs):
        step_id = self.kwargs['step_id']
        step = CITaskConfigService.task_step(step_id)
        stage = CITaskConfigService.task_stage(step.stage_id)
        parameter_groups = CITaskParameterService.task_parameter_list(stage.task_id)
        for group in parameter_groups:
            CITaskParameterService.save_step_settings(str(group.id))
        return self.destroy(request, *args, **kwargs)



class CITaskStageListView(generics.ListCreateAPIView):
    """
    get:
         path:/api/ci/task/<task_id>/stages

    post:
         path:/api/ci/task/<task_id>/stages

    """
    serializer_class = ci_serializer.CITaskStageSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        queryset = CITaskConfigService.task_stage_list(task_id)
        return queryset


class CITaskConfigView(generics.ListCreateAPIView):
    """
    get:
         path:/api/ci/task/<id>/config
         id:taskid
    put:
         path:/api/ci/task/<id>/config
         id:taskid
    """
    serializer_class = ci_serializer.CITaskStageSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        result=dict()
        task_id = int(self.kwargs['task_id'])
        default_stage = CITaskConfigService.task_default_sage(task_id)
        default_stage_serializer = ci_serializer.CITaskDefaultStageSerializer(instance=default_stage)
        queryset = CITaskConfigService.task_stage_list(task_id)
        serializer = self.get_serializer(queryset, many=True)
        result['base_info'] = default_stage_serializer.data
        result['config_stages'] = serializer.data
        return Response(result)


    def post(self, request, *args, **kwargs):
        task_id = int(self.kwargs['task_id'])
        config_stages = request.data.get('config_stages',None)
        if config_stages is not None:
            for stage in config_stages:
                temp_serializer = self.get_serializer(data=stage)
                temp_serializer.is_valid()
                temp_serializer._saving_instances = False
                instance = CITaskConfigService.task_stage(stage.get('id'))
                instance = temp_serializer.recursive_save(temp_serializer.validated_data,instance)
                instance.save()
                for step in stage.get('steps',[]):
                    temp_serializer = ci_step_serializer.CITaskStepSerializer(data=step)
                    temp_serializer.is_valid()
                    temp_serializer._saving_instances = False
                    instance = CITaskConfigService.task_step(step.get('id'))
                    instance = temp_serializer.recursive_save(temp_serializer.validated_data, instance)
                    instance.save()
            parameter_groups = CITaskParameterService.task_parameter_list(task_id)
            for group in parameter_groups:
                CITaskParameterService.save_step_settings(str(group.id))
        return Response(config_stages,status=status.HTTP_201_CREATED)


class CITaskRunStatusView(generics.CreateAPIView,generics.RetrieveAPIView):
    """
    post:
         path:/api/ci/task/step_status
    get: path: /api/ci/task/<tq_id>/done
    """
    serializer_class = ci_taskhistory_serializer.CITaskOutputSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        out_put = CITaskHistoryService.save_step_log(request.data)
        serializer = ci_taskhistory_serializer.CITaskOutputSerializer(instance=out_put)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, *args, **kwargs):
        tq_id = self.kwargs.get("tq_id", "")
        task_history = CITaskHistory.objects.get_by_tqid(int(tq_id))
        CITaskHistoryService.save_build_log(tq_id)
        CITaskHistoryService.clean_build_history(task_history.id)
        CITQService.update_task_queue_status(request)
        CITaskService.send_task_enqueue_message()
        return Response({"message","task_done"}, status=status.HTTP_201_CREATED)

class CITaskOutputListView(generics.ListCreateAPIView):
    """
    post:path:/api/ci/task/output/create
    get: path: /api/ci/task/<task_id>/outputs?
         FilterSet: id, TaskID,StageID,StageHistoryID,TaskHistoryID FilterOperation:=,__in,__gt,__contains,__icontains,Range__in,__lt,!=,__isnull
    """
    serializer_class = ci_taskhistory_serializer.CITaskOutputSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        task_history_id = int(self.kwargs.get("task_history_id",0))
        qs = CITaskStepOutput.objects.get_task_history_output(task_history_id)
        return CITaskStepOutPutFilterSet(data=self.request.GET, queryset=qs).filter()


class CITaskOutputView(generics.RetrieveAPIView):
    """
    get: path: /api/ci/task/output/<output_id>
    """
    serializer_class = ci_taskhistory_serializer.CITaskOutputSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        output_id = int(self.kwargs.get("output_id",0))
        output = CITaskStepOutput.objects.get(output_id)
        return output


class CITaskOutputUploadView(generics.CreateAPIView):
    """
    post:path:/api/ci/task/output/upload
    """
    serializer_class = ci_taskhistory_serializer.CITaskOutputSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):
        output_file = CITaskHistoryService.upload_package(request)
        serializer = ci_taskhistory_serializer.CITaskOutputSerializer(instance=output_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class CITaskOutputDownloadView(generics.RetrieveAPIView,generics.UpdateAPIView):
    """
    get:path:/api/ci/task/output/<output_id>/download
    patch:path:/api/ci/task/output/<output_id>/qrcode
    put:path:/api/ci/task/output/<output_id>/prepare
    """
    serializer_class = ci_taskhistory_serializer.CITaskOutputSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def put(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        output_id = int(self.kwargs.get("output_id", 0))
        output = CITaskStepOutput.objects.get(output_id)
        if output:
            if 'MAC' in user_agent.upper():
                FileInfoService.create_package_plist(output.id)
                # FileInfoService.create_package_file(output.id)
                package = WEB_HOST.replace('http', 'https') + "/static/plist_files/" + str(output.id) + ".plist"
            else:
                package = WEB_HOST + "/api/ci/task/output/" + str(output_id) + "/download"
        return Response({"package_url":package})

    def patch(self, request, *args, **kwargs):
        try:
            output_id = self.kwargs.get('output_id',0)
            code_image = QRCodeHelper.save_qr_code_stream(WEB_HOST+"/ci/task/output/" + str(output_id) + "/download")
            response = HttpResponse(code_image, content_type="image/png")
        except Exception as ex:
            SimpleLogger.exception(ex)
        return response

    def get(self, request, *args, **kwargs):
        result = HttpResponse({"message":"no file found"})
        try:
            output_id = int(self.kwargs.get("output_id", 0))
            output = CITaskStepOutput.objects.get(output_id)
            if output and output.ProductID:
                result = self.get_file_stream(output.ProductID)
        except Exception as ex:
            result = HttpResponse(str(ex))
            SimpleLogger.exception(ex)
        return result

    def get_file_stream(self,file_id):
        file = FileInfo.objects.get(int(file_id))
        contents = FileInfoService.download_file(file_id)

        def file_iterator(chunk_size=1024 * 50):
            while True:
                c = contents.read(chunk_size)
                if c:
                    yield c
                else:
                    break

        result = StreamingHttpResponse(file_iterator(), content_type='application/octet-stream')
        result['Content-Disposition'] = 'attachment;filename="' + file.FileName + '"'
        return result


class CITaskOutputQRCodeView(generics.RetrieveAPIView):
    """
    get:path:/api/ci/task/output/<output_id>/download
    patch:path:/api/ci/task/output/<output_id>/qrcode
    put:path:/api/ci/task/output/<output_id>/prepare
    """
    serializer_class = ci_taskhistory_serializer.CITaskOutputSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        try:
            output_id = self.kwargs.get('output_id',0)
            code_image = QRCodeHelper.save_qr_code_stream(WEB_HOST+"/ci/task/output/" + str(output_id) + "/download")
            response = HttpResponse(code_image, content_type="image/png")
        except Exception as ex:
            SimpleLogger.exception(ex)
        return response












    




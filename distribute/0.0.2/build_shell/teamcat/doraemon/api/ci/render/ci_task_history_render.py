#coding=utf-8
'''
Created on 2016-9-29

@author: zhangtiande
'''

from collections import OrderedDict
from rest_framework.renderers import JSONRenderer

from business.ci.ci_task_history_service import CITaskHistoryService
from doraemon.api.ci.serializer.ci_serializer import CITaskHistorySerializer

class CITaskHistoryListRenderer(JSONRenderer):
    
    
    def __init__(self):
        JSONRenderer.__init__(CITaskHistoryListRenderer)
        self.code=1
        self.message="test"
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        new_data=self.render_new_data(data, renderer_context)
        return JSONRenderer.render(self, new_data, accepted_media_type, renderer_context)
    
    
    def render_new_data(self,data,renderer_context):
        new_data=OrderedDict()
        detail_data=OrderedDict()
        task_id=int(renderer_context['kwargs']['task_id'])
        detail_data['latest_code_version']=CITaskHistoryService.get_latest_codeversion(task_id)
        detail_data['all_histories']=data
        new_data['code']=renderer_context['response'].status_code
        new_data['message']=renderer_context['response'].status_text
        new_data['result']=detail_data
        return new_data
        

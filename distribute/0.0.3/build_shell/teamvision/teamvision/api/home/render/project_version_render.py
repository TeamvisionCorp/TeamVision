#coding=utf-8
'''
Created on 2016-9-29

@author: zhangtiande
'''

from collections import OrderedDict
from rest_framework.renderers import JSONRenderer

from business.project.version_service import VersionService

class ProjectVersionListRenderer(JSONRenderer):
    
    
    def __init__(self):
        JSONRenderer.__init__(ProjectVersionListRenderer)
        self.code=1
        self.message="test"
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        new_data=self.render_new_data(data, renderer_context)
        return JSONRenderer.render(self, new_data, accepted_media_type, renderer_context)
    
    
    def render_new_data(self,data,renderer_context):
        new_data=OrderedDict()
        detail_data=OrderedDict()
        project_id=int(renderer_context['kwargs']['project_id'])
        detail_data['latest_version']=self.get_latest_version(project_id)
        detail_data['all_versions']=data
        new_data['code']=self.code
        new_data['message']=self.message
        new_data['result']=detail_data
        return new_data
    
    def get_latest_version(self,project_id):
        result='--'
        latest_version=VersionService.get_latest_version(project_id)
        if latest_version:
            result=latest_version.id
        return result
        

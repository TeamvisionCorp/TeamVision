#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.ci.pagefactory.ci_pageworker import CIPageWorker
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath

from teamvision.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker

from teamvision.ci.pagefactory.ci_plugin_pageworker import CIPluginPageWorker
from gatesidelib.common.simplelogger import SimpleLogger


class CISectionPageWorker(CIPageWorker):
    '''
    项目页面生成
    '''
   
    def __init__(self, request):
        '''
        Constructor
        '''
        CIPageWorker.__init__(self, request)
    
    
    def get_section_webpart(self, section,task_id):
        result = ""
        try:
            sorted_plugins = self.get_sorted_plugins(section)
            plugin_worker = CIPluginPageWorker(self.request)
            for plugin in sorted_plugins:
                if plugin.__contains__('plugin_id'):
                    plugin_id = int(plugin['plugin_id'])
                    result = result + plugin_worker.get_plugin(plugin, plugin_id,task_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    
    def get_sorted_plugins(self, section):
        plugins = section['plugins']
        plugins.sort(key=lambda x:x["order"], reverse=False)
        return plugins
        
        
            
            
        
        
    
    
    
    
    
        
        
        
        
    

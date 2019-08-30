#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.ci.viewmodels.plugins.vm_ci_plugin import VM_CIPlugin
from teamvision.ci.models import CITaskPlugin
from teamvision.ci.pagefactory.ci_template_path import CIPluginPath


class VM_XCodeSettingCheckPlugin(VM_CIPlugin):
    '''
    classdocs
    '''

    plugin_id=13
    
    def __init__(self,plugin_parameter_dict):
        VM_CIPlugin.__init__(VM_XCodeSettingCheckPlugin,plugin_parameter_dict)
        self.plugin=CITaskPlugin.objects.get(VM_XCodeSettingCheckPlugin.plugin_id)
        self.CFBundleIdentifier=self.get_parameter_value('CFBundleIdentifier')
        self.CFBundleShortVersionString=self.get_parameter_value('CFBundleShortVersionString')
        self.CFBundleVersion=self.get_parameter_value('CFBundleVersion')
        self.MinimumOSVersion=self.get_parameter_value('MinimumOSVersion')
        self.ipafileFilter=self.get_parameter_value('ipafileFilter')
        


        
    def get_template_path(self):
        return CIPluginPath.xcode_settings_check
    
    
    
   
    
    
    
                
        
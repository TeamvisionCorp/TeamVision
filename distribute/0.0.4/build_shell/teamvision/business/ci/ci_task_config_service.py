#coding=utf-8
'''
Created on 2016-7-6

@author: zhangtiande
'''
from business.business_service import BusinessService
from teamvision.ci.models import CITaskConfig,CITask
from teamvision.ci.models import BasicSection,SCMSection,PreBuildSection,PostBuildSection,BuildSection
from gatesidelib.common.simplelogger import SimpleLogger

class CITaskConfigService(object):
    '''
    classdocs
    '''
        
    
    @staticmethod
    def create_config():
        ci_task_config_dict=CITaskConfigService.init_task_config()
        doc_id=CITaskConfig.objects.save(ci_task_config_dict)
        return doc_id
    
    @staticmethod
    def copy_config(config_id,task_id,task_name):
        ci_task_config_dict=CITaskConfigService.get_ci_task_config(config_id)
        for parameter in ci_task_config_dict['basic_section']['plugins'][0]['parameter']:
            if parameter['name']=="id":
                parameter['value']=task_id
            if parameter['name']=="TaskName":
                parameter['value']=task_name    
        ci_task_config_dict.pop('_id')
        doc_id=CITaskConfig.objects.save(ci_task_config_dict)
        return doc_id
    
    @staticmethod
    def delete_config(config_id):
        CITaskConfig.objects.remove(config_id)
    
    
    @staticmethod
    def get_ci_task_config(config_id):
        task_config_dict= CITaskConfig.objects.get(config_id)
        return task_config_dict
    
    @staticmethod
    def get_ci_task_config_by_taskid(task_id):
        config_id=CITask.objects.get(task_id).TaskConfig
        task_config_dict= CITaskConfig.objects.get(config_id)
        return task_config_dict
    
    
    @staticmethod
    def init_task_config():
        task_config=CITaskConfig()
        task_config.basic_section=BasicSection().__dict__
        task_config.pre_section=PreBuildSection().__dict__
        task_config.scm_section=SCMSection().__dict__
        task_config.build_section=BuildSection().__dict__
        task_config.post_section=PostBuildSection().__dict__
        return task_config.__dict__
    
    @staticmethod
    def save_task_config(request,ci_task):
        config_section_dict=eval(request.POST.get('section'))
        SimpleLogger.info(config_section_dict)
        if config_section_dict.__contains__("basic_section"):
            CITaskConfigService.save_basic_section(config_section_dict.get('basic_section'), ci_task)
        
        if config_section_dict.__contains__("pre_section"):
            CITaskConfigService.save_pre_section(config_section_dict.get('pre_section'), ci_task.TaskConfig)
        
        if config_section_dict.__contains__("scm_section"):
            CITaskConfigService.save_scm_section(config_section_dict.get('scm_section'),ci_task.TaskConfig)
        
        if config_section_dict.__contains__("build_section"):
            CITaskConfigService.save_build_section(config_section_dict.get('build_section'), ci_task.TaskConfig)
        
        if config_section_dict.__contains__("post_section"):
            CITaskConfigService.save_post_section(config_section_dict.get('post_section'), ci_task.TaskConfig)
    
    
    @staticmethod
    def save_basic_section(basic_section,ci_task):
        print(basic_section)
        SimpleLogger.info(basic_section)
        parameter_map=basic_section[0].get('parameter')
        for item in parameter_map:
            if item.get('name')=="Description":
                ci_task.Description=item.get('value')
            if item.get('name')=="ci_task_project":
                ci_task.Project=item.get('value')
            if item.get('name')=="TaskName":
                ci_task.TaskName=item.get('value')
            if item.get('name')=="DeployService":
                ci_task.DeployService=item.get('value')
            
            if item.get('name')=="HistoryCleanStrategy":
                ci_task.HistoryCleanStrategy=item.get('value')

            if item.get('name')=="time_trigger":
                if CITaskConfigService.get_parameter_value(parameter_map,'ci_task_trigger')=='on':
                    ci_task.Schedule=item.get('value')
                else:
                    ci_task.Schedule=None
        ci_task.save()
        ci_task_config=CITaskConfigService.get_ci_task_config(ci_task.TaskConfig)
        ci_task_config['basic_section']['plugins']=basic_section
        CITaskConfig.objects.save(ci_task_config)

    @staticmethod
    def get_parameter_value(parameter_map,parameter_key):
        result=""
        for item in parameter_map:
            if item.get('name')==parameter_key:
                result=item.get('value')
        return result

        
    @staticmethod
    def save_scm_section(scm_section,config_id):
        ci_task_config=CITaskConfigService.get_ci_task_config(config_id)
        ci_task_config['scm_section']['plugins']=scm_section
        SimpleLogger.info("++++++++++++++++++++++++++++++++++++++++")
        SimpleLogger.info(scm_section)
        CITaskConfig.objects.save(ci_task_config)
    
    @staticmethod
    def save_build_section(build_section,config_id):
        ci_task_config=CITaskConfigService.get_ci_task_config(config_id)
        ci_task_config['build_section']['plugins']=build_section
        CITaskConfig.objects.save(ci_task_config)
    
    @staticmethod
    def save_pre_section(pre_section,config_id):
        ci_task_config=CITaskConfigService.get_ci_task_config(config_id)
        ci_task_config['pre_section']['plugins']=pre_section
        CITaskConfig.objects.save(ci_task_config)
    
    @staticmethod
    def save_post_section(post_section,config_id):
        ci_task_config=CITaskConfigService.get_ci_task_config(config_id)
        print(ci_task_config)
        ci_task_config['post_section']['plugins']=post_section
        CITaskConfig.objects.save(ci_task_config)    
    
    
    

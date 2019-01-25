#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from business.business_service import BusinessService
from doraemon.ci.models import CIDeployService
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from doraemon.project.models import Product,Project,Tag
from business.project.project_service import ProjectService
from doraemon.ci.mongo_models import CIServiceMongoFile
from business.common.mongodb_service import MongoDBService
from doraemon.home.models import FileInfo
from doraemon.ci.mongo_models import DeployServiceReplaceConfig,ReplaceFileMap
from bson import ObjectId

class CIService(BusinessService):
    '''
    classdocs
    '''
    
    
    
    @staticmethod
    def get_products_include_me(request):
        my_projects=ProjectService.get_projects_include_me(request)
        prodcut_ids=list()
        for project in my_projects:
            if project.Product not in prodcut_ids:
                prodcut_ids.append(project.Product)
        return Product.objects.all().filter(id__in=prodcut_ids)
    
    
    @staticmethod
    def get_product_ci_services(request,product_id):
        result=list()
        if product_id.upper()=="ALL":
            result=CIDeployService.objects.all().order_by('-id')
        else:
            product_projects=Project.objects.all().filter(Product=int(product_id))
            result=CIDeployService.objects.all().filter(Project__in=product_projects).order_by('-id')
        return result
                
    
    
    @staticmethod
    def create_ci_service(request):
        ci_service=CIDeployService()
        ci_service=CIService.init_ci_service(request, ci_service)
        ci_service.IsActive=1
        ci_service.save()
        CIService.log_create_activity(request.user, ci_service)
        return ci_service
    
    @staticmethod
    def edit_ci_service(request,service_id):
        ci_service=CIDeployService.objects.get(service_id)
        ci_service=CIService.init_ci_service(request, ci_service)
        ci_service.save()
        CIService.log_change_activity(request.user, ci_service)
    
    @staticmethod       
    def save_replace_config(request,service_id):
        if request.method=='POST':
            print(request.POST)
            ci_service=CIDeployService.objects.get(service_id)
            if ci_service.AdvanceConfig:
                replace_config=DeployServiceReplaceConfig.objects.get(id=ObjectId(ci_service.AdvanceConfig))
                replace_config=CIService.init_replace_config(request, replace_config)
                replace_config.save()
            CIService.log_change_activity(request.user, ci_service)
            
    @staticmethod
    def get_replace_config(congfig_id):
        return DeployServiceReplaceConfig.objects.get(id=ObjectId(congfig_id))
    
    @staticmethod
    def init_replace_config(request,replace_config):
        service_replace=replace_config
        file_id=request.POST.get('file_id',0)
        index=0
        for target in service_replace.replace_target_map:
            if target.file_id==int(file_id):
                temp_target=CIService.init_replace_targets(request, target)
                service_replace.replace_target_map[index]=temp_target
                service_replace.save()
                break
            index=index+1
        return service_replace
    
    @staticmethod
    def init_replace_targets(request,target):
        temp_target=target
        temp_target.file_id=request.POST.get('file_id',0)
        temp_target.file_name=request.POST.get("file_name","")
        temp_target.replace_targets=request.POST.get("replace_targets","")
        return temp_target
        
    
    @staticmethod
    def remove_replace_target(file_id,replace_config):
        index=0
        result=None
        for target in replace_config.replace_target_map:
            if target.file_id==int(file_id):
                result=target
                break
            index=index+1
        if result:
            replace_config.replace_target_map.remove(result)
        return replace_config
        
            
    
    
    
    @staticmethod
    def delete_ci_service(user,ci_serviceid):
        ci_service=CIDeployService.objects.get(int(ci_serviceid))
        ci_service.IsActive=0
        ci_service.save()
        CIService.log_delete_activity(user,ci_service)
    
    @staticmethod
    def copy_ci_service(user,ci_serviceid):
        ci_service=CIDeployService.objects.get(int(ci_serviceid))
        temp_service=ci_service
        temp_service.id=None
        temp_service.save()
        CIService.log_create_activity(user,ci_service)

    @staticmethod
    def init_ci_service(request,ci_service):
        tmp_ci_service=ci_service
        tmp_ci_service.ServiceName=request.POST.get('ServiceName')
        tmp_ci_service.Project=request.POST.get('ci_service_project',0)
        tmp_ci_service.AccessLog=request.POST.get('AccessLog',"")
        tmp_ci_service.DeployDir=request.POST.get('DeployDir',"")
        tmp_ci_service.DeployScripts=request.POST.get('DeployScripts',"")
        tmp_ci_service.ErrorLog=request.POST.get('ErrorLog',"")
        tmp_ci_service.RestartCommand=request.POST.get('RestartCommand',"")
        tmp_ci_service.StartCommand=request.POST.get('StartCommand',"")
        tmp_ci_service.StopCommand=request.POST.get('StopCommand',"")
        return tmp_ci_service
    
    
    @staticmethod
    def update_property(request,serviceid):
        service=CIDeployService.objects.get(serviceid)
        service.Tags=request.POST.get("Tags")
        update_fields=list()
        for field in request.POST:
            update_fields.append(field)
        service.save(update_fields=update_fields)
        CIService.log_change_property_activity(request.user,service,update_fields[0])
    
    @staticmethod
    def get_avalible_menu_tags():
        return Tag.objects.all().filter(TagType__in=[1,2])
    
    @staticmethod
    def get_agent_filter__tags():
        return Tag.objects.all().filter(TagType__in=[3])
    
    
    @staticmethod
    def file_upload_handler(request,service_id):
        
        #添加文件信息到服务
        message=""
        mongo_file_id=CIService.save_to_mongo(request)
        file_info_id,file_name=CIService.add_file(request,0, mongo_file_id)
        temp_service=CIDeployService.objects.get(int(service_id))
        if temp_service.RelatedFiles:
            temp_service.RelatedFiles=temp_service.RelatedFiles+str(file_info_id)+","
        else:
            temp_service.RelatedFiles=str(file_info_id)+","
        
        #上传文件后,创建默认的替换配置
        if temp_service.AdvanceConfig:
            replace_config=DeployServiceReplaceConfig.objects.get(id=ObjectId(temp_service.AdvanceConfig))
        else:
            replace_config=DeployServiceReplaceConfig()
        replace_config.service_id=int(service_id)
        target=ReplaceFileMap()
        target.file_id=file_info_id
        target.file_name=file_name
        replace_config.replace_target_map.append(target)
        
        #保存替换配置到服务
        temp_service.AdvanceConfig=replace_config.save().id
        temp_service.save()
        if file_info_id!=0:
            message=str(file_info_id)
        return message
        
    
    @staticmethod
    def delete_service_file(request,file_id):
        
        #删除service 相关文件信息，以及替换配置信息
        service_id=int(request.POST.get("service_id"))
        ci_service=CIDeployService.objects.get(service_id)
        ci_service.RelatedFiles=ci_service.RelatedFiles.replace(str(file_id)+',','')
        
        #删除替换配置
        service_replace_config=DeployServiceReplaceConfig.objects.get(id=ObjectId(ci_service.AdvanceConfig))
        CIService.remove_replace_target(file_id, service_replace_config)
        service_replace_config.save()
        ci_service.save()
        
        #从mongodb 删除文件
        file_info=FileInfo.objects.get(file_id)
        CIServiceMongoFile.objects.delete_file(file_info.FilePath)
        file_info.IsActive=0
        file_info.save()
        
        
        
    
    @staticmethod
    def get_service_file(request,mongo_file_id):
        return CIServiceMongoFile.objects.get(mongo_file_id)
    
    @staticmethod
    def save_to_mongo(request):
        result=0
        upload_file=request.FILES['service_file']
        if CIService.validate_upload_file(upload_file):
            result=MongoDBService.save_file(upload_file,CIServiceMongoFile)
        return result
    
    @staticmethod
    def add_file(request,folder_id,file_mongo_id):
        file_info=FileInfo()
        file_info.FileCreator=request.user.id
        file_info.FileFolder=folder_id
        file_info.FileName=CIServiceMongoFile.objects.get(file_mongo_id).metadata['file_real_name']
        file_info.FilePath=file_mongo_id
        file_info.FileSuffixes=CIService.get_file_suffixes(file_info.FileName)
        file_info.FileType=1
        file_info.save()
        return file_info.id,file_info.FileName
    
    
    @staticmethod
    def get_file_suffixes(file_name):
        length=len(file_name.split('.'))
        file_suffixes=file_name.split('.')[length-1]
        return file_suffixes
    
    @staticmethod
    def validate_upload_file(upload_file):
        result=False
        if upload_file.size<=50*1024*1024:
            result=True
        else:
            result=False
        return result
        

    @staticmethod
    def log_create_activity(user,ci_service):
        CIDeployService.objects.log_action(user.id,ci_service.id,ci_service.ServiceName,ADDITION,"创建了新服务",ci_service.Project,CIService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,ci_service):
        CIDeployService.objects.log_action(user.id,ci_service.id,ci_service.ServiceName,DELETION,"删除了服务",ci_service.Project,CIService.ActionLogType.CI)
    
    @staticmethod
    def log_change_activity(user,ci_service):
        CIDeployService.objects.log_action(user.id,ci_service.id,ci_service.ServiceName,CHANGE,"修改了服务",ci_service.Project,CIService.ActionLogType.CI)
        
        
        
        
#coding=utf-8
'''
Created on 2016-10-25

@author: zhangtiande
'''

from doraemon.home.models import FileInfo
from business.business_service import BusinessService
from doraemon.api.ci.mongo_models import PackgeMongoFile
import threading,os,shutil
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.settings import WEB_HOST,ROOT_DIR
from doraemon.ci.models import CITaskHistory
from model_managers import mongo_model


class FileInfoService(BusinessService):
    '''
    classdocs
    '''


    @staticmethod
    def add_file(folder_id,file_mongo_id,file_name,file_type,creator,file_size):
        file_info=FileInfo()
        file_info.FileCreator=creator
        file_info.FileFolder=folder_id
        file_info.FileName=file_name
        file_info.FilePath=file_mongo_id
        file_info.FileSuffixes=FileInfoService.get_file_suffixes(file_name)
        file_info.FileType=file_type
        file_info.FileSize=(file_size/1024)+1
        file_info.save()
        return file_info.id
    
    @staticmethod
    def get_file(file_id,mongo_object):
        result=None
        file=FileInfo.objects.get(int(file_id))
        if file:
            result=mongo_object.objects.get(file.FilePath)
        return result
    
    
    @staticmethod
    def get_file_content(file_id,mongo_object):
        result=""
        file=FileInfo.objects.get(int(file_id))
        if file:
            result=mongo_object.objects.get(file.FilePath).read().decode('utf-8')    
        return result
    
    @staticmethod
    def copy_file(file_id,source_model,target_model):
        target_file=FileInfoService.get_file(file_id,source_model)
        mongo_file_id=target_model.objects.copy_bucket(target_file)
        file=FileInfo.objects.get(int(file_id))
        file.id=None
        file.FilePath=mongo_file_id
        file.save()
        return file.id
    
    
    @staticmethod
    def clean_build_archive(file_id):
        worker=threading.Thread(target=FileInfoService.archive_clean_worker,args=(file_id,))
        worker.start()
        
        
    @staticmethod
    def archive_clean_worker(file_id):
        try:
            FileInfoService.delete_file(file_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        
    
    @staticmethod
    def delete_file(file_id,mongo_model=PackgeMongoFile):
        file=FileInfo.objects.get(int(file_id))
        if file:
            mongo_model.objects.delete_file(file.FilePath)
        file.IsActive=0
        file.save()
        
    @staticmethod
    def delete_value(file_id):
        file=FileInfo.objects.get(int(file_id))
        if file:
            PackgeMongoFile.objects.delete_value(file.FilePath)
        file.IsActive=0
        file.save()
        
    @staticmethod
    def download_file(file_id,mongo_model=PackgeMongoFile):
        file_info=FileInfo.objects.get(int(file_id))
        return mongo_model.objects.get(file_info.FilePath)
    
    
    
    @staticmethod
    def create_package_file(file_id,mongo_model=PackgeMongoFile):
        file_path=(ROOT_DIR+"/"+"static/ipa_files/"+str(file_id)+".ipa").replace("\\","/")
        if not os.path.exists(ROOT_DIR+"/"+"static/ipa_files"):
            os.mkdir(ROOT_DIR+"/"+"static/ipa_files")
        if not os.path.exists(file_path):
            file_info=FileInfo.objects.get(int(file_id))
            contents=mongo_model.objects.get(file_info.FilePath)
            ipa_file=open(file_path,'wb')
            ipa_file.write(contents.read())
            ipa_file.close()
    
    @staticmethod
    def create_package_plist(file_id,history_id):
        history=CITaskHistory.objects.get(int(history_id))
        template_file_path=ROOT_DIR+"/"+"static/plist_files/plist.plist"
        file_path=ROOT_DIR+"/"+"static/plist_files/"+str(file_id)+".plist"
        if history.PackageInfo:
            package_info=eval(history.PackageInfo)
            if not os.path.exists(file_path):
                shutil.copy(template_file_path,file_path)
                template_file=open(template_file_path,'rb')
                content=template_file.read().decode('utf-8')
                template_file.close()
                real_file=open(file_path,'wb')            
                content=content.replace('${PACKAGEURL}',WEB_HOST+"/static/ipa_files/"+str(file_id)+".ipa")
                content=content.replace('${APPID}',package_info['identifier'])
                content=content.replace('${APPVERSION}',package_info['shortVersion'])
                content=content.replace('${APPNAME}',package_info['name'])
                real_file.write(content.encode('utf-8'))
                real_file.close()
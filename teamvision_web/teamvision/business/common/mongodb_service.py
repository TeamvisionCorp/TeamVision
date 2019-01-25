#coding=utf-8
'''
Created on 2016-4-7

@author: zhangtiande
'''
import uuid
from gatesidelib.mongodb_helper import MongodbHelper
from teamvision.settings import MONGODB

class MongoDBService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def save_file(upload_file,mongo_file_object):
        file_property=mongo_file_object()
        file_property.file_real_name=upload_file.name
        file_property.content_type=MongoDBService.get_file_suffixes(file_property.file_real_name)
        file_property.file_name=str(uuid.uuid4())
        file_id=mongo_file_object.objects.save_bucket(upload_file.chunks(),file_property.file_name,file_property.__dict__)
        result=file_id
        return result
    @staticmethod
    def save_content_asfile(file_name,content,mongo_file_object):
        file_property=mongo_file_object()
        file_property.file_real_name=file_name
        file_property.content_type=MongoDBService.get_file_suffixes(file_property.file_real_name)
        file_property.file_name=str(uuid.uuid4())
        file_id=mongo_file_object.objects.save_content(content,file_property.file_name,file_property.__dict__)
        result=file_id
        return result
    
    @staticmethod
    def save(db,collection,value):
        HOST=MONGODB['default']['HOST']
        PORT=MONGODB['default']['PORT']
        mongo_helper=MongodbHelper(HOST,PORT)
        return mongo_helper.save(db,collection, value)
    
    @staticmethod
    def get(db,collection,doc_id):
        HOST=MONGODB['default']['HOST']
        PORT=MONGODB['default']['PORT']
        mongo_helper=MongodbHelper(HOST,PORT)
        result=mongo_helper.get(db,collection, doc_id)
        if result==None:
            result=mongo_helper.get('doraemon','ci', doc_id)
        return result

    @staticmethod
    def get_file_suffixes(file_name):
        length=len(file_name.split('.'))
        file_suffixes=file_name.split('.')[length-1]
        return file_suffixes
        
        
    
        
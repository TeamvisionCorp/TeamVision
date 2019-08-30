#coding=utf-8
'''
Created on 2017年9月4日

@author: ethan
'''
from model_managers.mongo_model.mongo_model_manager import MongoFileManager
from model_managers.mongo_model.mongo_model import MongoFile
from teamvision.settings import MONGODB

class FortestingMongoFile(MongoFile):
    HOST=MONGODB['project_documents']['HOST']
    PORT=MONGODB['project_documents']['PORT']
    DB=MONGODB['project_documents']['DB']
    objects=MongoFileManager(HOST,PORT,DB,"fortesting_doc")
        
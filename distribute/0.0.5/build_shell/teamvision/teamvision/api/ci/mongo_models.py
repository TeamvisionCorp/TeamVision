#coding=utf-8
'''
Created on 2017年9月4日

@author: zhangtiande
'''

from model_managers.mongo_model.mongo_model_manager import MongoFileManager
from model_managers.mongo_model.mongo_model import MongoFile
from teamvision.settings import MONGODB

class PackgeMongoFile(MongoFile):
    DB=MONGODB['archive']['DB']
    PORT=MONGODB['archive']['PORT']
    HOST=MONGODB['archive']['HOST']
    objects=MongoFileManager(HOST,PORT,DB,"build_package")

class BuildLogMongoFile(MongoFile):
    DB=MONGODB['archive']['DB']
    PORT=MONGODB['archive']['PORT']
    HOST=MONGODB['archive']['HOST']
    objects=MongoFileManager(HOST,PORT,DB,"build_log")

class ReleaseArchiveMongoFile(MongoFile):
    DB=MONGODB['release_archive']['DB']
    PORT=MONGODB['release_archive']['PORT']
    HOST=MONGODB['release_archive']['HOST']
    objects=MongoFileManager(HOST,PORT,DB,"release_archive")
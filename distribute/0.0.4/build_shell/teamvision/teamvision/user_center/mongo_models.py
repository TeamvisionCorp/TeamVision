#coding=utf-8
'''
Created on 2017年9月4日

@author: ethan
'''

from teamvision.settings import MONGODB


from model_managers.mongo_model import mongo_model_manager
from model_managers.mongo_model.mongo_model import MongoFile


class UCenterMongoFile(MongoFile):
    HOST=MONGODB['default']['HOST']
    PORT=MONGODB['default']['PORT']
    DB=MONGODB['default']['DB']
    objects=mongo_model_manager.MongoFileManager(HOST,PORT,DB,"ucenter_avatar")
#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from doraemon.project.models import Tag
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from gatesidelib.color_helper import ColorHelper

class TagService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def create_tag(tag_name,tag_type,owner_id):
        try:
            dm_tag=Tag()
            dm_tag.TagName=tag_name
            dm_tag.TagOwner=owner_id
            dm_tag.TagProjectID=0
            dm_tag.TagVisableLevel=1
            dm_tag.TagType=int(tag_type)
            dm_tag.TagColor=ColorHelper.random_color()
            dm_tag.save()
        except Exception as ex:
            print(ex)
            SimpleLogger.error(ex)
    
    @staticmethod
    def edit_tag(tag_name,tag_id):
        try:
            dm_tag=Tag.objects.get(tag_id)
            dm_tag.TagName=tag_name
            dm_tag.save()
        except Exception as ex:
            print(ex)
            SimpleLogger.error(ex)
            
        
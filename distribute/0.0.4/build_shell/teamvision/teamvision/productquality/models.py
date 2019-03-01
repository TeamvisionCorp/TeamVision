#coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''
from django.db import models


class BugFreeMapping(models.Model):
    ''' bugfree module id mapping table for
        doraemon project name
    '''
    DoraemonProjectID=models.IntegerField()
    DoraemonProjectName=models.CharField(max_length=500)
    DoraemonPlatformID=models.IntegerField()
    BugfreeProjectID=models.IntegerField()
    BugfreeProjectName=models.CharField(max_length=500)
    class Meta:
        app_label='productquality'
        db_table='bugfreemapping'
    


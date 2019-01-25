#coding=utf-8
'''
Created on 2016-1-13

@author: zhangtiande
'''

from django.db import connection
from dataaccess.auth_user.auth_user_sql import Permission

class DAL_Permission(object):
    '''
    classdocs
    '''
    
    
    @staticmethod
    def get_all_custom_permission():
        cursor = connection.cursor()
        cursor.execute(Permission.select_permission)
        rows = cursor.fetchall()
        return rows
        
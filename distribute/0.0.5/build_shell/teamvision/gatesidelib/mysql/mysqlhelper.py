#coding=utf-8
#coding=utf-8
'''
Created on 2015-2-3

@author: Devuser
'''
import mysql.connector
from gatesidelib.common.simplelogger import SimpleLogger

class MysqlHelper(object):
    '''
    mysql 访问帮助类
    '''
    
    def __init__(self,user,password,host,port,database):
        self.username=user
        self.passwd=password
        self.hostname=host
        self.port=port
        self.database=database
    
    def execute_query(self,sqlText):
        result=list()
        try:
            cnx = mysql.connector.connect(self.username,self.passwd,self.hostname,self.port,self.database)
            cursor = cnx.cursor()
            cursor.execute(sqlText)
            for row in cursor:
                result.append(row)
        except Exception,ex:
            SimpleLogger.logger.error(ex)
        finally:
            cnx.close()
        return result
    
    
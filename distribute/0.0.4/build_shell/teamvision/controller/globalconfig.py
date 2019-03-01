#coding=utf-8
'''
Created on 2014.1.15

@author: zhangtiande
'''
import platform

class GlobalConfig(object):
    '''
     global configs
    '''
    DEFAULTSERVERPORT=8080
    SERVERHOST="localhost"
    SSLSERVERPORT=443
    BASEDIR="E:\\coding_net\\doraemon_nirvana_lte\\doraemon"
    HANDLERPACKAGE='agent.business.driver.'
    
    @staticmethod
    def getslash():
        if platform.system()=="Windows":
            return "\\"
        else:
            return "/"
    
    @staticmethod
    def get_handler_package_path():
        return GlobalConfig.BASEDIR+GlobalConfig.getslash()+"agent"+GlobalConfig.getslash()+"business"+GlobalConfig.getslash()+"driver"
        
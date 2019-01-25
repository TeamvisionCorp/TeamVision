#coding=utf-8
'''
Created on 2016-3-10

@author: Devuser
'''

from gatesidelib.socket_helper.socket_server import SocketServer
from agent.request_handlers.socket_handler import SocketHandler
from agent.globalconfig import GlobalConfig
from gatesidelib.common.simplelogger import SimpleLogger
from agent.request_handlers.driver_pool import DriverPool

if __name__ == '__main__':
    host=GlobalConfig.SERVERHOST
    port=GlobalConfig.DEFAULTSERVERPORT
    SimpleLogger.info("start server ["+host+"] with port["+str(port)+"]")
    try:
        driver_pool=DriverPool()
        tcp_server=SocketServer.get_default_server(host,port,SocketHandler)
        SocketServer.start_server(tcp_server)
    except Exception as ex:
        SimpleLogger.info("start server ["+host+"] with port["+str(port)+"] fail")
        SimpleLogger.error(str(ex))
#coding=utf-8
'''
Created on 2014-11-27

@author: Devuser
'''
import logging
import logging.config
from teamvision.settings import LOG_CONFIG


class SimpleLogger(object):
    logging.config.fileConfig(LOG_CONFIG)
    
    @staticmethod
    def error(error_message):
        logger=logging.getLogger("errorlogger")
        logger.error(error_message)
    
    @staticmethod
    def info(info_message):
        logger=logging.getLogger("infologger")
        logger.info(info_message)
    
    @staticmethod
    def exception(ex):
        logger=logging.getLogger("errorlogger")
        logger.exception(ex)
         
    
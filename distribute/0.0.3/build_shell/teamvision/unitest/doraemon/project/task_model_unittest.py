#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

# from doraemon.project.models import Version
import cgitb
import unittest
from gatesidelib.common.simplelogger import SimpleLogger
from unitest.doraemon.exception_test.TestException import TestException


class Test():
    
    
    def error_log(self):
        try:
            TestException.exception_1()
            
        except Exception as ex:
            SimpleLogger.exception(ex)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test=Test()
    test.error_log()
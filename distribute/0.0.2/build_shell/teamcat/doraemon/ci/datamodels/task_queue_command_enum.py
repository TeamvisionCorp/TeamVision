#coding=utf-8
'''
Created on 2014-5-15

@author: ETHAN
'''

class TaskQueueCommandTypeEnum(object):
    '''
    all task status enum value for test task
    '''
    TaskQueueCommandType_Start=1
    TaskQueueCommandType_Stop=2
    TaskQueueCommandType_SendResultEmail=4
    TaskQueueCommandType_RerunCase=5

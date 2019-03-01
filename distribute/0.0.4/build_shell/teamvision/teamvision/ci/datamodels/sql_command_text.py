#coding=utf-8
'''
Created on 2016-12-1

@author: Administrator
'''

class CITaskSQL(object):
    
    last_build_tasks="select * from ( select distinct t2.* from ci_task t2 inner join ci_task_history t3 on t2.id=t3.CITaskID  and t3.IsActive=1 and t2.IsActive=1 and  t2.id in ${TASKIDS}) t4 order by id desc"
        
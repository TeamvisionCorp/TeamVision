#coding=utf-8
'''
Created on 2016-1-13

@author: zhangtiande
'''

class Permission(object):
    select_permission=("select t1.id, t1.name,t2.Description,t2.PermissionType from auth_permission t1 "
    "inner join auth_permission_extend t2 on t2.permission_id=t1.id "
    "order by t2.PermissionType")
#coding=utf-8
'''
Created on 2015-11-11

@author: zhangtiande
'''

class Project(object):
    
    project_save_filed="项目保存失败，请联系管理员"
    project_member_save_fail="添加成员失败，请重试"
    project_member_remove_fail="删除成员失败，请重试"
    project_member_update_role_fail="更新成员角色失败，请重试"
    project_webhook_save_fail="添加webhook失败，请重试"
    project_webhook_remove_fail="删除webhook失败，请重试"
    project_webhook_set_default_fail="必须有一个默认的WebHook"
    project_webhook_perform_fail="尝试发送请求失败，请检查url,参数是否正确"
    

class Fortesting(object):
    
    fortesting_save_fail="提测保存失败请联系管理员"
    fortesting_build_fail="构建请求失败请联系管理员"
    fortesting_commit_fail="提测失败请联系管理员"


class Version(object):
    
    version_save_fail="版本添加失败请联系管理员"
    version_delete_fail="版本删除失败请联系管理员"
    version_update_fail="版本更新失败请联系管理员"
    
class Module(object):
    
    module_save_fail="模块添加失败请联系管理员"
    module_delete_fail="模块删除失败请联系管理员"
    module_update_fail="模块更新失败请联系管理员"


class Task(object):
    task_save_fail="任务创建失败,请联系管理员"
    task_delete_fail="任务删除失败,请联系管理员"
    task_update_progress_fail="进度更新失败,请稍后重试"

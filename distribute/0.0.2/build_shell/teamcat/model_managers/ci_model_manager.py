# coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from model_managers.model_manager import ModelManager
from gatesidelib.mongodb_helper import MongodbHelper
from doraemon.settings import MONGODB


class CIPluginManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CIPluginManager, self).get_queryset().filter(IsActive=1)

    def get(self, plugin_id):
        return super(CIPluginManager, self).get_queryset().get(id=plugin_id)


class CITaskManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CITaskManager, self).get_queryset().filter(IsActive=1)

    def get(self, task_id):
        result = None
        try:
            result = super(CITaskManager, self).get_queryset().get(id=task_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def project_tasks(self, project_id):
        result = None
        try:
            result = self.all().filter(Project=project_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class CITaskFlowManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CITaskFlowManager, self).get_queryset().filter(IsActive=1)

    def get(self, flow_id):
        result = None
        try:
            result = super(CITaskFlowManager, self).get_queryset().get(id=flow_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def project_taskflows(self, project_id):
        result = None
        try:
            result = self.all().filter(Project=project_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class CITaskFlowSectionManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CITaskFlowSectionManager, self).get_queryset().filter(IsActive=1)

    def get(self, section_id):
        result = None
        try:
            result = super(CITaskFlowSectionManager, self).get_queryset().get(id=section_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def flow_sections(self, flow_id):
        result = None
        try:
            result = self.all().filter(TaskFlow=flow_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class CITaskFlowHistoryManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CITaskFlowHistoryManager, self).get_queryset().filter(IsActive=1)

    def flow_history(self,flow_id):
        return  self.all().filter(TaskFlow = flow_id)

    def get(self, history_id):
        result = None
        try:
            result = super(CITaskFlowHistoryManager, self).get_queryset().get(id=history_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class CIFlowSectionHistoryManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CIFlowSectionHistoryManager, self).get_queryset().filter(IsActive=1)

    def flow__section_history(self,flow_history_id):
        return  self.all().filter(TaskFlowHistory = flow_history_id)

    def get(self, history_id):
        result = None
        try:
            result = super(CIFlowSectionHistoryManager, self).get_queryset().get(id=history_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result





class CITaskHistoryManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self, is_active=1):
        if is_active == 1:
            return super(CITaskHistoryManager, self).get_queryset().filter(IsActive=is_active)
        else:
            return super(CITaskHistoryManager, self).get_queryset()

    def get(self, history_id, is_active=1):
        return self.all(is_active).get(id=history_id)

    def get_by_tqid(self, tq_id):
        result = None
        try:
            result = self.all().filter(TaskQueueID=tq_id)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_task_history(self, task_id, is_active=1):
        result = None
        try:
            result = self.all(is_active).filter(CITaskID=task_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_history_by_tq(self, tq_id):
        result = list()
        try:
            result = self.all().filter(TaskQueueID=tq_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result[0]

    def get_history_by_sechistory(self,sec_history_id,is_active=1):
        result = list()
        try:
            result = self.all(is_active).filter(FlowSectionHistory=sec_history_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


    def get_history_by_uuid(self, uuid):
        result = list()
        try:
            result = self.all().filter(TaskUUID=uuid)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result[0]


class AutoTaskResultManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(AutoTaskResultManager, self).get_queryset().filter(IsActive=1)

    def get(self, result_id):
        return self.all().get(id=result_id)

    def get_by_historyid(self, history_id):
        result = None
        try:
            result = self.all().filter(TaskHistoryID=history_id).filter(ParentResultID=0)[0]
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class AutoCaseResultManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(AutoCaseResultManager, self).get_queryset()

    def get(self, result_id):
        result = None
        try:
            self.all().get(id=result_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_by_resultid(self, result_id, result_type):
        result = list()
        try:
            result = self.all().filter(TaskResultID=result_id)
            if int(result_type) != 0:
                result = result.filter(Result=int(result_type))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class UnitTestCaseResultManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(UnitTestCaseResultManager, self).get_queryset()

    def get(self, result_id):
        return self.all().get(id=result_id)

    def get_by_task_result(self, result_id, result_type):
        result = list()
        try:
            result = self.all().filter(TaskResultID=result_id)
            if int(result_type) != 0:
                result = result.filter(Result=int(result_type))
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class AutoCaseManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(AutoCaseManager, self).get_queryset()

    def get(self, case_id):
        result = None
        try:
            result = self.all().get(id=case_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_by_project(self, Project_id, case_type=None):
        '''
           case_type:filter case by case_type. case_type is a list.like:[1,2] 
        '''
        result = None
        try:
            result = self.all().filter(ProjectID=Project_id)
            if case_type:
                result = result.filter(CaseType__in=case_type)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class CaseTagManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CaseTagManager, self).get_queryset()

    def get(self, tag_id):
        return self.all().get(id=tag_id)


class ServiceHostManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(ServiceHostManager, self).get_queryset().filter(IsActive=1)

    def get(self, service_id):
        return self.all().get(id=service_id)

    def get_by_envid(self, env_id):
        '''
           case_type:filter case by case_type. case_type is a list.like:[1,2] 
        '''
        result = list()
        try:
            result = self.all().filter(EnvID=env_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result


class CICredentialsManager(ModelManager):
    '''
    classdocs
    '''
    use_in_migrations = True

    def all(self):
        return super(CICredentialsManager, self).get_queryset().filter(IsActive=1)

    def get(self, task_id):
        return super(CICredentialsManager, self).get_queryset().get(id=task_id)

    def get_public_credentials(self):
        return self.all().filter(Scope=1)

    def get_my_credentials(self, user_id):
        return self.all().filter(Creator=user_id)


class CIDeployServiceManager(ModelManager):
    '''
    classdocs
    '''
    db = MONGODB['default']['DB']
    port = MONGODB['default']['PORT']
    host = MONGODB['default']['HOST']
    collection = "ci_deployservice"
    default_db = "doraemon"
    default_collection = "ci"

    def all(self):

        return super(CIDeployServiceManager, self).get_queryset().filter(IsActive=1)

    def get(self, service_id):
        result = None
        try:
            result = super(CIDeployServiceManager, self).get_queryset().get(id=service_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def save_replace_config(self, value):
        mongo_helper = MongodbHelper(CIDeployServiceManager.host, CIDeployServiceManager.port)
        return mongo_helper.save(CIDeployServiceManager.db, CIDeployServiceManager.collection, value)

    def get_replace_config(self, doc_id):
        mongo_helper = MongodbHelper(CIDeployServiceManager.host, CIDeployServiceManager.port)
        result = mongo_helper.get(CIDeployServiceManager.db, CIDeployServiceManager.collection, doc_id)
        if result == None:
            result = mongo_helper.get(CIDeployServiceManager.default_db, CIDeployServiceManager.default_collection,
                                      doc_id)
        return result


class CITaskConfigManager(object):

    def __init__(self, mongo_host, mongo_port, db, collection):
        self.host = mongo_host
        self.port = mongo_port
        self.db = db
        self.collection = collection
        self.default_db = "doraemon"
        self.default_collection = "ci"
        self.mongo_helper = MongodbHelper(self.host, self.port)

    def save(self, value):
        return self.mongo_helper.save(self.db, self.collection, value)

    def remove(self, doc_id):
        result = self.mongo_helper.remove(self.db, self.collection, doc_id)
        if result == None:
            result = self.mongo_helper.remove(self.default_db, self.default_collection, doc_id)
        return result

    def get(self, doc_id):
        result = self.mongo_helper.get(self.db, self.collection, doc_id)
        if result == None:
            result = self.mongo_helper.get(self.default_db, self.default_collection, doc_id)
        return result

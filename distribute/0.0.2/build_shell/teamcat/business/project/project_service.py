#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from doraemon.project.models import Project,ProjectMember,Product,ProjectModule,Version
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from business.project.version_service import VersionService
from business.auth_user.user_service import UserService
import random

class ProjectService(object):
    '''
    classdocs
    '''


    @staticmethod
    def get_latest_projects_include_me(request):
        result = list()
        latest_projects = ProjectService.get_latest_projects(request)
        my_projects = ProjectService.get_projects_include_me(request)
        my_project_ids = [project.id for project in my_projects]
        for project in latest_projects:
            if project and  project.id in my_project_ids:
                result.append(project)
        return result[0:6]
    
    @staticmethod
    def get_latest_projects(request):
        result=list()
        latest_project_ids=VersionService.get_latests_project_ids(request)
        for project_id in latest_project_ids:
            temp_project=Project.objects.get(project_id)
            result.append(temp_project)
        return result
                
        
    @staticmethod
    def get_projects_include_me(request,product_id='all'):
        if product_id==None:
            product_id="0"
        if UserService.is_admin(request.user.id):
            return Project.objects.all()
        member_list= ProjectMember.objects.all().filter(PMMember=request.user.id)
        project_ids=[member.PMProjectID for member in member_list]
        if product_id.upper()=="ALL":
            result=Project.objects.all().filter(id__in=project_ids)
        else:
            result=Project.objects.all().filter(id__in=project_ids).filter(Product=int(product_id))
        return result
    
    @staticmethod
    def get_products_include_me(request):
        my_projects=ProjectService.get_projects_include_me(request)
        prodcut_ids=list()
        for project in my_projects:
            if project.Product not in prodcut_ids:
                prodcut_ids.append(project.Product)
        return Product.objects.all().filter(id__in=prodcut_ids)
        
    @staticmethod
    def get_project_modules(project_id):
        return ProjectModule.objects.project_modules(int(project_id))

    @staticmethod
    def create_project(request):
        try:
            project=Project()
            project=ProjectService.init_project(request.data, project)
            project.PBCreator=request.user.id
            project.save()
            if str(request.user.id)!=str(project.PBLead):
                ProjectService.add_member(request.user.id,project.id,5)
                ProjectService.add_member(project.PBLead,project.id,4)
            else:
                ProjectService.add_member(request.user.id,project.id,4)
            ProjectService.create_version(project,request.user)
            ProjectService.log_create_activity(request.user, project)
        except Exception as ex:
            SimpleLogger.error(ex)

    @staticmethod
    def create_version(project,user):
        version=Version()
        version.VProjectID=project.id
        version.VVersion='1.0.0'
        version.CFTCommitor=user.id
        version.save()
        VersionService.log_create_activity(user, version)




    @staticmethod
    def edit_project(request,projectid):
        temp_project=Project.objects.get(projectid)
        project=ProjectService.init_project(request.POST, temp_project)
        project.save()
        ProjectService.log_change_activity(request.user, project)
    
    
    @staticmethod
    def delete_project(request,projectid):
        print(projectid)
        project=Project.objects.get(projectid)
        project.IsActive=0
        project.save()
        ProjectService.log_delete_activity(request.user, project)
        
    
    @staticmethod
    def init_project(validate_data,project):
        tmp_project=project
        tmp_project.PBTitle=validate_data.get('PBTitle')
        tmp_project.PBDescription=validate_data.get('PBDescription')
        tmp_project.PBKey=validate_data.get('PBKey')
        tmp_project.PBPlatform=validate_data.get('PBPlatform')
        tmp_project.PBVisiableLevel=validate_data.get('PBVisiableLevel')
        tmp_project.PBLead=validate_data.get('PBLead')
        tmp_project.Product=1
        tmp_project.PBHttpUrl=validate_data.get('PBHttpUrl')
        tmp_project.PBAvatar="/static/global/images/project-icon/scenery-"+str(random.randint(1, 24))+".png"
        return tmp_project
    
    @staticmethod
    def add_member(user,projectid,Role):
        project_member=ProjectMember()
        project_member.PMProjectID=projectid
        project_member.PMMember=user
        project_member.PMRoleID=Role
        project_member.PMRoleType=1
        project_member.save()
    
    @staticmethod
    def log_create_activity(user,project):
        Project.objects.log_action(user.id,project.id,project.PBTitle,ADDITION,"创建了项目",project.id)
    
    @staticmethod
    def log_delete_activity(user,project):
        Project.objects.log_action(user.id,project.id,project.PBTitle,DELETION,"删除了项目",project.id)
    
    @staticmethod
    def log_change_activity(user,project):
        Project.objects.log_action(user.id,project.id,project.PBTitle,CHANGE,"修改了项目",project.id)
        
        
        
        
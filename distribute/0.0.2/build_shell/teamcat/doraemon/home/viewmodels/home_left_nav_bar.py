#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''
from business.auth_user.user_service import UserService
from doraemon.home.models import FileInfo


class HomeLeftNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request):
        self.request=request
        self.project_href='/home/project/all'
        self.autotask_href='/home/autotask/all'
        self.fortesting_href='/home/my/fortesting'
        self.task_href=    '/home/my/task'
        self.webapps_href='/home/webapps/all'
        self.device_href='/home/device/all'
        self.issue_href='/home/issue/1'
    
    
    def login_user(self):
        result=None
        if self.request.user:
            result=UserService.get_user(self.request.user.id)
        return result
    
    def login_user_avatar(self):
        result="/static/global/images/caton/caton1.jpeg"
        if self.login_user():
            if self.login_user().extend_info.avatar.isdigit():
                avatar_path=FileInfo.objects.get(int(self.login_user().extend_info.avatar))
                result="/ucenter/account/get_avatar/"+avatar_path.FilePath
            else:
                result=self.login_user().extend_info.avatar
        return result
#         self.version_href='/project/'+str(projectid)+'/version/all'

class HomeProjectLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.request=request
        if args['sub_nav_action']!='all':
            self.project_href='/home/product/'+args['sub_nav_action']+'/project'
        self.project_active="leftmeunactive"
        self.custom_menu_list=list()
        
class HomeDashboardLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.request=request
        self.dashboard_active="leftmeunactive"
        self.custom_menu_list=list()

class HomeAutoTestingTaskLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.task_href='/home/autotask/'+args['sub_nav_action']
        self.request=request
        self.autotask_active="leftmeunactive"
        self.custom_menu_list=list()



class HomeForTestingLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.request=request
        self.fortesting_href='/home/fortesting/'+args['sub_nav_action']
        self.fortesting_active="leftmeunactive"
        self.custom_menu_list=list()

class HomeIssueLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.request=request
        self.issue_href='/home/issue/'+args['sub_nav_action']
        self.issue_active="leftmeunactive"
        self.custom_menu_list=list()



class HomeTaskLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.request=request
        self.task_href='/home/task/'+args['sub_nav_action']
        self.task_active="leftmeunactive"
        self.custom_menu_list=list()
        
class HomeWebAppsLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.request=request
        self.webapps_active="leftmeunactive"
        self.webapps_href='/home/webapps/'+args['sub_nav_action']
        self.custom_menu_list=list()

class HomeDeviceLeftNavBar(HomeLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        HomeLeftNavBar.__init__(self,request)
        self.request=request
        self.device_active="leftmeunactive"
        self.device_href='/home/device/all'
        self.custom_menu_list=list()

    
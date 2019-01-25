# coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from teamvision.project.models import TestApplication, Project, Version, WebHook, ProjectModule, ProjectCodeUrl
from teamvision.project.mongo_models import FortestingMongoFile
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION, CHANGE, ADDITION
from gatesidelib.datetimehelper import DateTimeHelper
from business.common.system_config_service import SystemConfigService
from business.ci.ci_task_service import CITaskService
from business.auth_user.user_service import UserService
from business.business_service import BusinessService
from business.project.project_service import ProjectService
from business.common.mongodb_service import MongoDBService
from business.common.file_info_service import FileInfoService

from teamvision.settings import EMAIL_TEMPLATES
from teamvision.project.viewmodels.vm_project_fortesting import VM_ProjectForTesting


class ForTestingService(BusinessService):
    '''
    classdocs
    '''

    @staticmethod
    def get_my_fortestings(request):
        my_project_ids = list()
        my_products = ProjectService.get_products_include_me(request).order_by('-id')
        for product in my_products:
            projects = ProjectService.get_projects_include_me(request, str(product.id)).order_by('-id')
            my_project_ids.extend([project.id for project in projects])
        result = ForTestingService.get_projects_fortestings(my_project_ids)
        return result

    @staticmethod
    def get_projects_fortestings(project_ids):
        '''
            get testapplications form projects which is joined by me
        '''
        return TestApplication.objects.all().filter(ProjectID__in=project_ids).order_by("-id")

    @staticmethod
    def get_project_fortestings(project_id):
        '''
            get testapplications form  one project which is joined by me
        '''
        result = TestApplication.objects.all().order_by("-id")
        if project_id != "0":
            result = TestApplication.objects.all().filter(ProjectID=project_id).order_by("-id")
        return result

    @staticmethod
    def create_fortesting(form_data, user):
        result = None
        try:
            for_testing = TestApplication()
            for_testing = ForTestingService.init_fortesting(form_data, for_testing)
            for_testing.Creator = user.id
            for_testing.Status = 1
            for_testing.save()
            branch = form_data.get('Branch')
            code_repertory = form_data.get('CodeRepertory')
            for_testing.ProjectCode = ForTestingService.create_project_code(for_testing.ProjectCode, for_testing.id,
                                                                            code_repertory, branch)
            for_testing.save()
            ForTestingService.log_create_activity(user, for_testing)
            result = for_testing
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    @staticmethod
    def edit_fortesting(form_data, user, fortesting_id):
        for_testing = TestApplication.objects.get(fortesting_id)
        for_testing = ForTestingService.init_fortesting(form_data, for_testing)
        for_testing.save()
        branch = form_data.get('Branch')
        code_repertory = form_data.get('CodeRepertory')
        for_testing.ProjectCode = ForTestingService.create_project_code(for_testing.ProjectCode, for_testing.id,
                                                                        code_repertory, branch)
        for_testing.save()
        ForTestingService.log_change_activity(user, for_testing)
        return for_testing

    @staticmethod
    def delete_fortesting(request, fortesting_id):
        for_testing = TestApplication.objects.get(fortesting_id)
        for_testing.PBIsActive = 0
        for_testing.save()
        ForTestingService.log_delete_activity(request.user, for_testing)

    @staticmethod
    def init_fortesting(form_data, for_testing):
        tmp_fortesting = for_testing
        project_id = form_data.get('ProjectID')
        if project_id:
            tmp_fortesting.ProjectID = form_data.get('ProjectID')
        tmp_fortesting.TestingFeature = form_data.get('TestingFeature')
        tmp_fortesting.TestingAdvice = form_data.get('TestingAdvice')
        tmp_fortesting.ProjectModuleID = form_data.get('ProjectModuleID', 0)
        tmp_fortesting.Attachment = ForTestingService.get_attachmeht_id(form_data)
        # tmp_fortesting.ExpectCommitDate=form_dat.get('ExpectCommitDate')
        tmp_fortesting.Topic = form_data.get('Topic')
        if not tmp_fortesting.VersionID:
            tmp_fortesting.VersionID = form_data.get('VersionID')
        return tmp_fortesting

    @staticmethod
    def get_attachmeht_id(form_data):
        attachments = form_data.get('attachments')
        result = ''
        for attachment in attachments['uploadList']:
            result = str(attachment['id']) + ',' + result
        return result

    @staticmethod
    def add_tester(fortesting_id, tester_id):
        fortesting = TestApplication.objects.get(int(fortesting_id))
        if int(tester_id) not in eval(fortesting.Testers):
            fortesting.Testers = fortesting.Testers + "," + tester_id
            fortesting.save();

    @staticmethod
    def remove_tester(fortesting_id, tester_id):
        fortesting = TestApplication.objects.get(int(fortesting_id))
        fortesting.Testers = fortesting.Testers.replace("," + tester_id, "")
        #         if len(fortesting.Testers)==1:
        #             fortesting.Testers=fortesting.Testers+","
        fortesting.save()

    @staticmethod
    def create_project_code(code_id, applicationid, codeurl, branch):
        result = code_id
        "".strip()
        if code_id == 0:
            if codeurl.strip() != "":
                tmp_code = ProjectCodeUrl()
                tmp_code.Branch = branch
                tmp_code.CodeRepertory = codeurl
                tmp_code.ApplicationID = applicationid
                tmp_code.save()
                result = tmp_code.id
            else:
                result = 0
        else:
            tmp_code = ProjectCodeUrl.objects.get(code_id)
            tmp_code.Branch = branch
            tmp_code.CodeRepertory = codeurl
            tmp_code.save()
        return result

    @staticmethod
    def create_version(version_id, version_number, projectid):
        result = version_id
        if version_id == None:
            tmp_version = Version()
            tmp_version.VVersion = version_number
            tmp_version.VProjectID = projectid
            tmp_version.save()
            result = tmp_version.id
        else:
            tmp_version = Version.objects.get(version_id)
            if tmp_version.VVersion.strip() != version_number.strip():
                new_version = Version()
                new_version = tmp_version
                new_version.id = None
                new_version.VVersion = version_number
                new_version.save()
                result = new_version.id
        return result

    @staticmethod
    def fortesting_build(request, fortesting_id):
        fortesting = TestApplication.objects.get(fortesting_id)
        webhook = WebHook.objects.get_build_webhook(fortesting.ProjectID)
        parameter_group_id = ""
        if webhook.WHParameters and "=" in webhook.WHParameters:
            parameter_group_id = webhook.WHParameters.split('=')[1]
        taskid = webhook.WHURL.strip('/').split('/')[-1:][0]
        CITaskService.start_ci_task(request, taskid, parameter_group_id, fortesting.VersionID)
        ForTestingService.log_build_activity(request.user, fortesting)

    @staticmethod
    def update_fortesting_status(login_user, fortesting_id, status):
        result = [False, '']
        fortesting = TestApplication.objects.get(fortesting_id)
        fortesting.Status = int(status)
        fortesting.save()
        if int(status) == 1:
            ForTestingService.fortesting_wait_for_commit(login_user, fortesting, status)
        if int(status) == 2:
            result = ForTestingService.fortesting_commit(login_user, fortesting, status)
        if int(status) == 3:
            ForTestingService.fortesting_intesting(login_user, fortesting, status)
        if int(status) == 4:
            ForTestingService.fortesting_finished(login_user, fortesting, status)
        if int(status) == 5:
            ForTestingService.fortesting_archive(login_user, fortesting, status)
        return result

    @staticmethod
    def fortesting_wait_for_commit(login_user, fortesting, status):
        pass

    @staticmethod
    def fortesting_archive(login_user, fortesting, status):
        pass

    @staticmethod
    def fortesting_commit(login_user, fortesting, status):
        message = "已经将项目提测信息，通知到项目成员。！"
        build_summary = "已经提测了！"
        result = [False, '']
        try:
            notification_status = (eval(fortesting.EmailNotificationStatus)[int(status) - 1] == 0)
            if notification_status:
                result[0] = True
                result[1] = message
                fortesting.CommitTime = DateTimeHelper.getcnow()
                fortesting.Commitor = login_user.id
                email_notification_status = ForTestingService.get_email_notification_status(
                    fortesting.EmailNotificationStatus, status)
                fortesting.EmailNotificationStatus = email_notification_status
                fortesting.save()
                email_template = EMAIL_TEMPLATES['ForTesting']
                ForTestingService.send_notification_email(fortesting.id, build_summary, email_template)
                ForTestingService.log_commit_activity(login_user, fortesting)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.exception(ex)
        return result

    @staticmethod
    def fortesting_intesting(login_user, fortesting, status):
        message = "任务开始测试通知，已经发送给所有项目成员！"
        build_summary = "已经开始测试了！"
        result = []
        try:
            notification_status = eval(fortesting.EmailNotificationStatus)[int(status) - 1] == 0
            if notification_status:
                result.append(notification_status)
                result.append(message)
                email_notification_status = ForTestingService.get_email_notification_status(
                    fortesting.EmailNotificationStatus, status)
                fortesting.EmailNotificationStatus = email_notification_status
                fortesting.Testers = fortesting.Testers + "," + str(login_user.id)
                fortesting.save()
                # email_template=EMAIL_TEMPLATES['InTesting']
                # ForTestingService.send_notification_email(fortesting.id,build_summary,email_template)
                ForTestingService.log_start_testing_activity(login_user, fortesting)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.exception(ex)
        return result

    @staticmethod
    def fortesting_finished(login_user, fortesting, status):
        message = "测试完成通知，已经发送给所有项目成员！"
        build_summary = "已经完成测试！"
        result = []
        try:
            notification_status = eval(fortesting.EmailNotificationStatus)[int(status) - 1] == 0
            if notification_status:
                email_notification_status = ForTestingService.get_email_notification_status(
                    fortesting.EmailNotificationStatus, status)
                fortesting.EmailNotificationStatus = email_notification_status
                fortesting.TestingFinishedDate = DateTimeHelper.getcnow()
                fortesting.save()
                # email_template=EMAIL_TEMPLATES['TestingFinished']
                # ForTestingService.send_notification_email(fortesting.id,build_summary,email_template)
                ForTestingService.log_finish_testing_activity(login_user, fortesting)
                result.append(notification_status)
                result.append(message)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.exception(ex)
        return result

    @staticmethod
    def set_start_end_date(fortesting_id, startdate, enddate):
        fortesting = TestApplication.objects.get(fortesting_id)
        fortesting.TestingStartDate = startdate
        fortesting.TestingDeadLineDate = enddate
        fortesting.save()

    @staticmethod
    def get_email_notification_status(old_status, status_item):
        result = ""
        old_status_list = old_status.split(',')
        old_status_list[int(status_item) - 1] = 1
        for item in old_status_list:
            result = result + str(item) + ","
        return result[:len(result) - 1]

    # @staticmethod
    # def fortesting_finish_build(request):
    #     message = "successful"
    #     build_summary="构建已经完成了！"
    #     try:
    #         fortesting_id = request.POST["id"]
    #         email_config = SystemConfigService.get_email_config()
    #         build_status = request.POST['buildstatus']
    #         fortesting = TestApplication.objects.get(fortesting_id)
    #         build_history=ForTestingService.add_build_history(request,fortesting)
    #         fortesting.CFTBuildID=build_history.id
    #         fortesting.save(update_fields=['CFTBuildID'])
    #         ForTestingService.send_notification_email(fortesting_id,build_summary,email_config['emailbuildtemplatepath'])
    #     except Exception as ex:
    #         message = str(ex)
    #         SimpleLogger.exception(ex)
    #     return message

    @staticmethod
    def attachments_upload_handler(file):
        message = []
        mongo_message = ForTestingService.save_to_mongo(file,FortestingMongoFile)
        if mongo_message[0] != "0":
            file_id = FileInfoService.add_file(0, mongo_message[0], file.name, 1, 0, file.size)
            message.append(file_id)
            message.append(mongo_message[0])
        else:
            message[0] = "0"
            message[1] = "长传文件失败，" + mongo_message[1]
        return message

    @staticmethod
    def download_attachment(file_id):
        return FileInfoService.get_file(file_id, FortestingMongoFile)

    @staticmethod
    def delete_file(file_id):
        FileInfoService.delete_file(file_id, mongo_model=FortestingMongoFile)


    @staticmethod
    def get_fortesting_version(fortesting):
        return Version.objects.get(fortesting.VersionID).VVersion

    @staticmethod
    def send_notification_email(fortesting_id, summary_info, email_tempalte_path):
        fortesting = TestApplication.objects.get(fortesting_id)
        email_list = ForTestingService.get_email_list(fortesting.ProjectID)
        email_config = SystemConfigService.get_email_config()
        email_message = ForTestingService.create_email_message(fortesting, summary_info, email_tempalte_path)
        projectname = Project.objects.get(fortesting.ProjectID).PBTitle
        subject = "项目：【" + projectname + "】" + summary_info
        ForTestingService.send_email(email_config, email_list, email_message, subject)

    @staticmethod
    def create_email_message(fortesting, summary_info, email_template_path):
        result = ""
        if fortesting.Status == 2:
            result = ForTestingService.create_commit_message(fortesting, summary_info, email_template_path)

        if fortesting.Status == 3:
            result = ForTestingService.create_intesting_message(fortesting, summary_info, email_template_path)

        if fortesting.Status == 4:
            result = ForTestingService.create_finished_message(fortesting, summary_info, email_template_path)

        return result

    @staticmethod
    def create_commit_message(fortesting, summary_info, email_template_path):
        email_templates = open(email_template_path, 'rb').read().decode()
        project = Project.objects.get(fortesting.ProjectID)
        projectname = project.PBTitle
        module = ProjectModule.objects.get(fortesting.ProjectModuleID)
        module_name = "--"
        code_addr = ProjectCodeUrl.objects.get(fortesting.ProjectCode)
        if module:
            module_name = module.Name
        platform = SystemConfigService.get_platform_name(project.PBPlatform)
        submitior = UserService.get_user(fortesting.Commitor)
        title = "项目：【" + platform + projectname + ForTestingService.get_fortesting_version(
            fortesting) + "】" + summary_info
        email_templates = email_templates.replace("${SUBMITIONINFO}", title)
        email_templates = email_templates.replace("${SUBMITTIME}", str(DateTimeHelper.getcnow()))
        email_templates = email_templates.replace("${SUBMITID}", str(fortesting.id))
        email_templates = email_templates.replace("${PROJECTNAME}", projectname)
        email_templates = email_templates.replace("${PROJECTMODULENAME}", module_name)
        email_templates = email_templates.replace("${SUBMITIOR}", str(submitior.last_name + submitior.first_name))
        email_templates = email_templates.replace("${PLATFORM}", str(platform))
        email_templates = email_templates.replace("${VERSION}", ForTestingService.get_fortesting_version(fortesting))
        if code_addr:
            email_templates = email_templates.replace("${CODEURI}", code_addr.CodeRepertory)
            email_templates = email_templates.replace("${BRANCH}", code_addr.Branch)
        else:
            email_templates = email_templates.replace("${CODEURI}", "")
            email_templates = email_templates.replace("${BRANCH}", "")
        email_templates = email_templates.replace("${FUNCTIONCHANGE}", str(fortesting.TestingFeature))
        email_templates = email_templates.replace("${SUGGESTION}", str(fortesting.TestingAdvice))
        return email_templates

    @staticmethod
    def create_intesting_message(fortesting, summary_info, email_template_path):
        email_templates = open(email_template_path, 'rb').read().decode()
        project = Project.objects.get(fortesting.ProjectID)
        submitior = UserService.get_user(fortesting.Commitor)
        version = ForTestingService.get_fortesting_version(fortesting)
        vm_fortesting = VM_ProjectForTesting(fortesting)
        tester_name = "--"
        if len(vm_fortesting.fortesting_testers()) > 0:
            tester_name = vm_fortesting.fortesting_testers()[0].member_name()
        title = "项目：【" + project.PBTitle + version + "】" + summary_info
        email_templates = email_templates.replace("${SUBMITIONINFO}", title)
        email_templates = email_templates.replace("${SUBMITTIME}", str(DateTimeHelper.getcnow()))
        email_templates = email_templates.replace("${TPID}", str(fortesting.id))
        email_templates = email_templates.replace("${PROJECTNAME}", project.PBTitle)
        email_templates = email_templates.replace("${STARTTIME}", str(vm_fortesting.testing_start_date()))
        email_templates = email_templates.replace("${ENDTIME}", str(vm_fortesting.testing_deadline()))
        email_templates = email_templates.replace("${SUBMITIOR}", str(submitior.last_name + submitior.first_name))
        email_templates = email_templates.replace("${TESTER}", tester_name)
        email_templates = email_templates.replace("${VERSION}", version)

        return email_templates

    @staticmethod
    def create_finished_message(fortesting, summary_info, email_template_path):
        email_templates = open(email_template_path, 'rb').read().decode()
        project = Project.objects.get(fortesting.ProjectID)
        submitior = UserService.get_user(fortesting.Commitor)
        version = ForTestingService.get_fortesting_version(fortesting)
        vm_fortesting = VM_ProjectForTesting(fortesting)
        tester_name = "--"
        if len(vm_fortesting.fortesting_testers()) > 0:
            tester_name = vm_fortesting.fortesting_testers()[0].member_name()
        title = "项目：【" + project.PBTitle + version + "】" + summary_info
        email_templates = email_templates.replace("${SUBMITIONINFO}", title)
        email_templates = email_templates.replace("${TPID}", str(fortesting.id))
        email_templates = email_templates.replace("${PROJECTNAME}", project.PBTitle)
        email_templates = email_templates.replace("${SUBMITIOR}", str(submitior.last_name + submitior.first_name))
        email_templates = email_templates.replace("${TESTER}", tester_name)
        email_templates = email_templates.replace("${VERSION}", version)
        email_templates = email_templates.replace("${FUNCTIONCHANGE}", str(fortesting.TestingFeature))
        email_templates = email_templates.replace("${SUGGESTION}", str(fortesting.TestingAdvice))

        return email_templates

    @staticmethod
    def log_create_activity(user, target):
        version = Version.objects.get(target.VersionID)
        project = Project.objects.get(target.ProjectID)
        TestApplication.objects.log_action(user.id, target.id, target.Topic, ADDITION,
                                           "创建了新提测", target.ProjectID)

    @staticmethod
    def log_delete_activity(user, target):
        version = Version.objects.get(target.VersionID)
        project = Project.objects.get(target.ProjectID)
        TestApplication.objects.log_action(user.id, target.id, target.Topic, DELETION,
                                           "删除了提测", target.ProjectID)

    @staticmethod
    def log_change_activity(user, target):
        version = Version.objects.get(target.VersionID)
        project = Project.objects.get(target.ProjectID)
        TestApplication.objects.log_action(user.id, target.id, target.Topic, CHANGE,
                                           "修改了提测", target.ProjectID)

    @staticmethod
    def log_commit_activity(user, target):
        version = Version.objects.get(target.VersionID)
        project = Project.objects.get(target.ProjectID)
        TestApplication.objects.log_action(user.id, target.id, target.Topic, 4, "提测了新版本",
                                           target.ProjectID)

    @staticmethod
    def log_start_testing_activity(user, target):
        version = Version.objects.get(target.VersionID)
        project = Project.objects.get(target.ProjectID)
        TestApplication.objects.log_action(user.id, target.id, target.Topic, 4, "开始测试",
                                           target.ProjectID)

    @staticmethod
    def log_finish_testing_activity(user, target):
        version = Version.objects.get(target.VersionID)
        project = Project.objects.get(target.ProjectID)
        TestApplication.objects.log_action(user.id, target.id, target.Topic, 4, "完成了测试",
                                           target.ProjectID)

    @staticmethod
    def log_build_activity(user, target):
        version = Version.objects.get(target.VersionID)
        project = Project.objects.get(target.ProjectID)
        TestApplication.objects.log_action(user.id, target.id, target.Topic, ADDITION,
                                           "构建了新包", target.ProjectID)

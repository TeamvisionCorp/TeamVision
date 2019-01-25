# coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''

from teamvision.project.models import IssueActivity, Project
from gatesidelib.common.simplelogger import SimpleLogger
from gatesidelib.datetimehelper import DateTimeHelper
from teamvision.project.models import ProjectIssue, IssueFilter
from teamvision.project.mongo_models import IssueMongoFile
from business.common.mongodb_service import MongoDBService
from business.common.system_config_service import SystemConfigService
from business.common.redis_service import RedisService
from business.common.file_info_service import FileInfoService
from django.contrib.admin.models import DELETION, CHANGE, ADDITION
from teamvision.project.viewmodels.vm_project_issue import VM_ProjectIssue
from business.auth_user.user_service import UserService
from teamvision.settings import EMAIL_TEMPLATES
from business.business_service import BusinessService
import xlwt,time
from teamvision.settings import WEB_HOST
from business.common.excel_file_service import ExcelFileService


class IssueService(ExcelFileService,BusinessService):
    '''
    classdocs
    '''

    @staticmethod
    def all_issues(project_id, user_id):
        result = IssueService.project_all_issues(project_id)
        filter_key = str(user_id) + "_issue_filter"
        if RedisService.has_key(filter_key):
            filter_values = RedisService.get_svalue(filter_key)
            result = IssueService.filter_all_issues(result, filter_values)
        result = IssueService.search_issue(result, user_id)
        return result

    @staticmethod
    def my_issue(user_id, issue_user_role=1):
        '''
           我的问题：不同角色关注不同的问题
           issue_user_role: 1:issue owner,2 issue creator,3 issue follower
        '''
        result = list()
        if str(issue_user_role) == "1":
            result = ProjectIssue.objects.get_processor_issue(user_id).filter(Status__in=(1,2))
        if str(issue_user_role) == "2":
            result = ProjectIssue.objects.get_reporter_issue(user_id)
        result = IssueService.search_issue(result, user_id)
        return result.order_by('-id')

    @staticmethod
    def search_issue(all_issue, user_id):
        key = str(user_id) + "_issue_searchkeyword"
        result = all_issue
        if RedisService.has_key(key):
            search_word = RedisService.get_value(key)
            result = result.filter(Title__icontains=search_word)
        return result

    @staticmethod
    def project_all_issues(project_id):
        result = ProjectIssue.objects.get_project_issue(int(project_id)).order_by("-id")
        return result

    @staticmethod
    def filter_all_issues(all_issue, filters):
        result = all_issue
        if len(filters):
            filter_string = IssueService.get_filter_string(filters)
            result = eval(filter_string)
        return result

    @staticmethod
    def get_filter_string(filters):
        filter_string = ""
        for filter_item in filters:
            filter_item_value = filter_item
            filter_field = filter_item_value.split(":")[0]
            filter_value = filter_item_value.split(":")[1]
            # if filter_field=="Team":
            #     continue
            if filter_value in ["0", "", "0,"]:
                continue
            if filter_field.endswith("_s"):
                filter_string = filter_string + "filter(" + filter_field.replace("_s",
                                                                                 "__in") + "=(" + filter_value + "))."
            else:
                if filter_field == "CreationTime":
                    start_date = filter_value[:11].strip()
                    end_date = filter_value[12:].strip()
                    filter_string = filter_string + "filter(" + filter_field + "__range=('" + start_date + "','" + end_date + "'))."
                else:
                    filter_string = filter_string + "filter(" + filter_field + "=" + filter_value + ")."
        filter_string = "ProjectIssue.objects.all()." + filter_string + "order_by('-id')"
        print(filter_string)
        return filter_string

    @staticmethod
    def search_all_issues(project_id, user_id, keyword):
        result = IssueService.all_issues(project_id, user_id)
        if keyword.strip() != "":
            result = result.filter(Title__icontains=keyword)
        return result

    @staticmethod
    def filter_value_dict(filter_key):
        result = dict()
        filter_values = RedisService.get_svalue(filter_key)
        for filter_item in filter_values:
            filter_item_value = filter_item
            print(filter_item_value)
            filter_field = filter_item_value.split(":")[0]
            filter_value = filter_item_value.split(":")[1]
            if filter_value == "":
                filter_value = "0,0"
            if filter_field.endswith("_s"):
                dict_key = filter_field.replace("_s", "")
                result[dict_key] = eval("[" + filter_value + "]")
            else:
                if filter_field == "CreationTime":
                    start_date = filter_value[:11].strip()
                    end_date = filter_value[12:].strip()
                    result[filter_field] = eval("['" + start_date + "','" + end_date + "']")
                else:
                    result[filter_field] = filter_value
        return result

    @staticmethod
    def create_issue(form_data,user):
        try:

            issue = ProjectIssue()
            issue = IssueService.init_issue(form_data, issue)
            print(form_data)
            issue.Creator = user.id
            issue.Status = 2
            issue.Solution = 1
            issue.save()
            # IssueService.send_notification_email(issue,"创建了新问题",EMAIL_TEMPLATES['Issue'])
            IssueService.create_issue_activity(issue, '','', '', "新问题", user.id, 1, 1)
            IssueService.log_create_activity(user, issue)
        except Exception as ex:
            SimpleLogger.error(ex)

    @staticmethod
    def send_notification_email(issue,summary_info,email_tempalte_path):
        processor = UserService.get_user(issue.Processor)
        email_list = [processor.email]
        email_config = SystemConfigService.get_email_config()
        email_message = IssueService.create_email_message(issue,summary_info,email_tempalte_path)
        project_name = Project.objects.get(issue.Project).PBTitle
        subject = "项目：【" + project_name + "】待处理问题通知"
        IssueService.send_email(email_config, email_list, email_message, subject)

    @staticmethod
    def create_email_message(issue, summary_info,email_template_path):
        email_templates = open(email_template_path, 'rb').read().decode()
        project= Project.objects.get(issue.Project)
        projectname = project.PBTitle
        issue_adress = WEB_HOST + '/' + '/project/' + str(issue.Project) + '/issue/' + str(issue.id)
        title="项目 ["+projectname+"] "+summary_info+" "+str(issue.id)
        email_templates = email_templates.replace("${SUBMITIONINFO}",title)
        email_templates = email_templates.replace("${TITLE}", issue.Title)
        email_templates = email_templates.replace("${ADDRESS}", issue_adress)
        return email_templates

    @staticmethod
    def update_issue(issue_id, field, value, new_text, user_id):
        result = False
        try:
            issue = ProjectIssue.objects.get(int(issue_id))
            old_value = str(issue.__dict__[field])
            if old_value != str(value):
                if field == "OSVersion":
                    temp = value.split(",")
                    issue.__dict__[field] = int(temp[0])
                    issue.__dict__['DeviceOS'] = int(temp[1])
                else:
                    issue.__dict__[field] = value
                issue.UpdateTime = DateTimeHelper.getcnow()
                issue.save()
                if field == 'Processor':
                    IssueService.send_notification_email(issue,"更新了问题",EMAIL_TEMPLATES['Issue'])
                result = True
                IssueService.create_issue_activity(issue, field, value, old_value, new_text, user_id, 2, 1)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    @staticmethod
    def update_issue_operation_result(issue_id, operation_type, solution, comments, user_id):
        result = False
        try:
            issue = ProjectIssue.objects.get(int(issue_id))
            if str(operation_type) == "1":  # 解决问题
                field = "Solution"
                old_value = str(issue.__dict__[field])
                issue.__dict__[field] = int(solution)
                issue.Status = 4
                issue.ResolvedTime = DateTimeHelper.getcnow()
                issue.UpdateTime = DateTimeHelper.getcnow()
                issue.Solver = user_id
                issue.Processor = issue.Creator
                issue.save()
                IssueService.send_notification_email(issue,"修复了问题",EMAIL_TEMPLATES['Issue'])
                IssueService.create_issue_activity(issue, field, "", "", "解决了问题", user_id, 2, 1)

            if str(operation_type) == "2":  # 关闭问题
                field = "Status"
                old_value = str(issue.__dict__[field])
                value = 3
                issue.Status = 3
                issue.Processor = issue.Creator
                issue.ClosedTime = DateTimeHelper.getcnow()
                issue.UpdateTime = DateTimeHelper.getcnow()
                issue.save()
                IssueService.create_issue_activity(issue, field, "", "", "关闭了问题", user_id, 2, 1)

            if str(operation_type) == "3":  # 重新打开问题
                field = "Status"
                old_value = str(issue.__dict__[field])
                value = 5
                if issue.Solver:
                    issue.Processor = issue.Solver
                else:
                    issue.Processor = user_id
                issue.ReopenCounts = issue.ReopenCounts + 1
                issue.UpdateTime = DateTimeHelper.getcnow()
                issue.Status = 5
                issue.save()
                IssueService.send_notification_email(issue,"重新打开了问题",EMAIL_TEMPLATES['Issue'])
                IssueService.create_issue_activity(issue, field, "", "", "重新打开了问题", user_id, 2, 1)

            if comments != "":
                IssueService.create_issue_activity(issue, 0, '', '', "备注" + comments, user_id, 1, 1)

            result = True
        except Exception as ex:
            SimpleLogger.error(ex)
        return result

    @staticmethod
    def create_issue_activity(issue, field, value, old_value, new_text, user_id, action_flag, action_type):
        '''
            action_type: 1 issue相关，2 comment
            action_flag: 1 新增，2 更新，3 删除
        '''
        activity = IssueActivity()
        activity.Creator = user_id
        if field == None:
            activity.FieldDesc = ""

        elif str(field) != "0":
            activity.FieldDesc = issue.get_field_verbose_name(field)
        else:
            activity.FieldDesc = "备注"
        activity.FieldName = field
        activity.OldValue = str(old_value).strip()
        activity.NewValue = str(value).strip()
        activity.Message = new_text.strip()
        activity.Issue = issue.id
        activity.ActionFlag = action_flag
        activity.ActionType = action_type
        activity.save()

    @staticmethod
    def create_issue_filter(project_id, filter_id, filter_name, user_id):
        if str(filter_id) == "0":
            temp_filter = IssueFilter()
        else:
            temp_filter = IssueFilter.objects.get(int(filter_id))
        temp_filter.Project = int(project_id)
        temp_filter.FilterName = filter_name
        temp_filter.Creator = int(user_id)
        filter_key = str(user_id) + "_issue_filter"
        if RedisService.has_key(filter_key):
            filter_values = RedisService.get_svalue(filter_key)
            temp_filter.FilterString = IssueService.get_filter_string(filter_values)
            temp_filter.FilterUIConfig = IssueService.filter_value_dict(filter_key)
            temp_filter.FilterCacheString = filter_values
        temp_filter.Scope = 1
        temp_filter.save()
        return temp_filter.id

    @staticmethod
    def init_issue(form_data, issue):
        tmp_issue = issue
        project = form_data.get('Project')[0]
        version = form_data.get('Project')[1]
        tmp_issue.Project = project
        tmp_issue.Version = version
        tmp_issue.Title = form_data.get("Title")
        tmp_issue.Processor = form_data.get("Processor")
        tmp_issue.Desc = form_data.get("Desc")
        tmp_issue.Team = form_data.get("Team", 0)
        tmp_issue.Module = form_data.get("Module")
        tmp_issue.IssueCategory = form_data.get("IssueCategory")
        tmp_issue.Severity = form_data.get("Severity")
        tmp_issue.ProjectPhase = form_data.get("ProjectPhase")
        tmp_issue.Priority = form_data.get("Priority")
        tmp_issue.DeviceOS = form_data.get("DeviceOS")
        cached_file_keys = form_data.get("uploadList")
        tmp_issue.Attachments = IssueService.store_cached_file(cached_file_keys)
        return tmp_issue

    @staticmethod
    def store_cached_file(cached_file_keys):
        result = ""
        keys = cached_file_keys
        for key in keys:
            if key != "":
                temp_file = RedisService.get_object(key)
                if temp_file != None:
                    RedisService.delete_value(key)
                    mongo_id = MongoDBService.save_file(temp_file, IssueMongoFile)
                    file_id = FileInfoService.add_file(0, mongo_id, temp_file.name, 1, 0, temp_file.size)
                    if file_id != 0:
                        result = result + str(file_id) + ","
        return result

    @staticmethod
    def cache_issue_attachments(upload_file,user):
        message = {"cache_key":"","message":"上传文件超过10M"}
        try:
            if RedisService.validate_upload_file(upload_file, 10 * 1024 * 1024, None):
                cached_key = str(user.id) + "_" + str(time.time())
                RedisService.set_object(cached_key, upload_file, 1800)
                message["cache_key"] = cached_key
        except Exception as ex:
            SimpleLogger.exception(ex)
            message["message"] = str(ex)
        return message

    @staticmethod
    def attachments_upload_handler(file):
        message = []
        mongo_message = IssueService.save_to_mongo(file, IssueMongoFile)
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
        return FileInfoService.get_file(int(file_id), IssueMongoFile)

    @staticmethod
    def delete_attachment(file_id,issue_id):
        FileInfoService.delete_file(int(file_id), mongo_model=IssueMongoFile)
        if int(issue_id) != 0:
            issue = ProjectIssue.objects.get(int(issue_id))
            issue.Attachments = issue.Attachments.replace(str(file_id)+",","")
            issue.save()


    @staticmethod
    def cache_issue_filter(key, values):
        field_name = values.split(":")[0]
        old_filter = RedisService.get_svalue(key)
        for item in old_filter:
            filter_member = item
            if filter_member.startswith(field_name):
                RedisService.delete_smember(key, filter_member)
        RedisService.set_svalue(key, values, 7 * 24 * 3600)

    @staticmethod
    def cache_issue_search_word(key, value):
        if RedisService.has_key(key):
            RedisService.delete_value(key)
            RedisService.set_value(key, value, 1800)
        else:
            RedisService.set_value(key, value, 1800)

    @staticmethod
    def update_issue_filter_cache(key, filter_id):
        RedisService.delete_value(key)
        if str(filter_id) != "0":
            filter = IssueFilter.objects.get(int(filter_id))
            if filter.FilterCacheString:
                for filter_item in eval(filter.FilterCacheString):
                    RedisService.set_svalue(key, filter_item, 7 * 24 * 3600)

    @staticmethod
    def filter_ui_config(filter_id):
        result = ""
        filter = IssueFilter.objects.get(int(filter_id))
        if filter:
            for item in eval(filter.FilterCacheString):
                result = result + item + ";"
        return result

    @staticmethod
    def issue_excel_file(issue_list, user_id):
        wb = xlwt.Workbook(encoding='utf-8')
        sheet_all = wb.add_sheet('ALL')
        sheet_all = IssueService.issue_all_sheet(sheet_all, issue_list, user_id)
        return wb

    @staticmethod
    def issue_all_sheet(excel_sheet, issue_list, user_id):
        all_issues = issue_list
        vm_issue_results = list()
        for issue in all_issues:
            temp_issue_result = VM_ProjectIssue(user_id, issue)
            vm_issue_results.append(temp_issue_result)
        excel_sheet = IssueService.get_issue_sheet(excel_sheet, vm_issue_results, ' 32')
        return excel_sheet

    @staticmethod
    def get_issue_sheet(excel_sheet, result_list, sheet_type):
        style_heading = IssueService.get_heading_style(sheet_type)
        style_body = IssueService.get_style_body()
        excel_sheet = IssueService.get_sheet_header(excel_sheet, style_heading)
        excel_sheet = IssueService.get_sheet_body(result_list, excel_sheet, style_body)
        return excel_sheet

    @staticmethod
    def get_sheet_header(excle_sheet, heading_style):
        excle_sheet.write(0, 0, '问题ID', heading_style)
        excle_sheet.write(0, 1, '问题主题', heading_style)
        excle_sheet.write(0, 2, '状态', heading_style)
        excle_sheet.write(0, 3, '报告人', heading_style)
        excle_sheet.write(0, 4, 'Owner', heading_style)
        excle_sheet.write(0, 5, '创建时间', heading_style)
        excle_sheet.write(0, 6, '解决结果', heading_style)
        excle_sheet.write(0, 7, '严重性', heading_style)
        excle_sheet.write(0, 8, '版本', heading_style)
        excle_sheet.write(0, 9, '链接', heading_style)
        return excle_sheet

    @staticmethod
    def get_sheet_body(result_list, excel_sheet, body_style):
        row = 1
        issue_id_style = IssueService.get_column_style('32')
        for result in result_list:
            issue_link = WEB_HOST + "/project/" + str(result.issue.Project) + "/issue/" + str(result.issue.id)
            excel_sheet.write(row, 0, result.issue.id, issue_id_style)
            excel_sheet.write(row, 1, result.default_title() + "  " + result.issue.Title, body_style)
            excel_sheet.write(row, 2, result.status().Name, body_style)
            excel_sheet.write(row, 3, result.creator_name(), body_style)
            excel_sheet.write(row, 4, result.processor_name(), body_style)
            excel_sheet.write(row, 5, str(result.issue.CreationTime), body_style)
            excel_sheet.write(row, 6, result.solution().Name, body_style)
            excel_sheet.write(row, 7, result.severity().Name, body_style)
            excel_sheet.write(row, 8, result.version(), body_style)
            excel_sheet.write(row, 9, issue_link, body_style)

            # 第一行加宽
            excel_sheet.col(0).width = 100 * 50
            excel_sheet.col(1).width = 200 * 50
            excel_sheet.col(2).width = 100 * 50
            excel_sheet.col(3).width = 100 * 50
            excel_sheet.col(4).width = 200 * 50
            excel_sheet.col(5).width = 300 * 50
            excel_sheet.col(6).width = 300 * 50
            excel_sheet.col(7).width = 300 * 50
            excel_sheet.col(8).width = 300 * 50
            excel_sheet.col(9).width = 300 * 50
            row += 1
        return excel_sheet

    @staticmethod
    def log_create_activity(user, target):
        IssueActivity.objects.log_action(user.id, target.id, target.Title, ADDITION, "创建了新问题", target.Project)

    @staticmethod
    def log_delete_activity(user, target):
        IssueActivity.objects.log_action(user.id, target.id, target.Title, DELETION, "删除了问题", target.Project)

    @staticmethod
    def log_change_activity(user, target):
        IssueActivity.objects.log_action(user.id, target.id, target.Title, CHANGE, "修改了问题", target.Project)

    @staticmethod
    def log_change_property_activity(user, target, filed_name):
        if filed_name == "Status":
            IssueActivity.objects.log_action(user.id, target.id, target.Title, CHANGE, "更新了问题状态", target.Project)
        else:
            IssueActivity.objects.log_action(user.id, target.id, target.Title, CHANGE, "修改了问题信息", target.Project)

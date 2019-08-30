#coding=utf-8
'''
Created on 2016-4-7

@author: zhangtiande
'''
from business.common.system_config_service import SystemConfigService
from business.project.memeber_service import MemberService
from gatesidelib.emailhelper import EmailHelper
from teamvision.settings import EMAILCONFIG
from business.common.mongodb_service import MongoDBService
import threading


class BusinessService(object):
    '''
    classdocs
    '''
    
    HOST=EMAILCONFIG['HOST']
    PORT=EMAILCONFIG['PORT']
    USER=EMAILCONFIG['USER']
    PASSWORD=EMAILCONFIG['PASSWORD']
    ISAUTH=EMAILCONFIG['ISAUTH']
    STARTSSL=EMAILCONFIG['STARTSSL']
    POSTFIX=EMAILCONFIG['POSTFIX']
    
    @staticmethod
    def get_file_suffixes(file_name):
        file_suffixes = ''
        length=len(file_name.split('.'))
        if "." in file_name:
            file_suffixes=file_name.split('.')[length-1]
        return file_suffixes
    
    
    @staticmethod
    def get_project_member_email_list(project_id,outputemaillist):
        email_list = outputemaillist
        members=MemberService.get_member_users(project_id)
        for member in members:
            if member.email in email_list:
                    pass
            else:
                email_list.append(member.email)
        return email_list
    
    @staticmethod
    def get_default_email_list(outputemaillist):
        email_list = outputemaillist
        email_config = SystemConfigService.get_email_config()
        emails = email_config['defautrecivers']
        for email in emails.split(','):
            if email in email_list:
                    pass
            else:
                email_list.append(email)
        return email_list
    
    @staticmethod
    def get_email_list(project_id):
        emaillist = BusinessService.get_project_member_email_list(project_id, [])
        emaillist = BusinessService.get_default_email_list(emaillist)
        return emaillist

    @staticmethod
    def send_email(emailconfig, emaillist, emailmessage, subject):
        email_config = SystemConfigService.get_email_config()
        print(email_config)
        emailSender = EmailHelper(email_config['Host'],email_config['User'] , email_config['Password'],
                                  email_config['Postfix'],email_config['Port'])
        message = emailSender.generatetextmessage(emailmessage, subject, ','.join(emaillist), 'html')
        if email_config['Password'].strip() !="":
            worker = threading.Thread(target=emailSender.sendemaillogin, args=(emaillist, subject, message.as_string()))
            worker.start()
        else:
            worker = threading.Thread(target=emailSender.sendmail_nologin,
                                      args=(emaillist, subject, message.as_string()))
            worker.start()
    
    
    @staticmethod
    def validate_upload_file(upload_file,size,file_type):
        '''
        upload_file: request.Files['upload_file']
        size: file size int
        file_type: ['png','jpg'] list
        '''
        result=False
        file_content_type=BusinessService.get_file_suffixes(upload_file.name)
        if upload_file.size<=size:
            result=True
        if file_type!=None:
            if result and  file_content_type in file_type:
                result=True
            else:
                result=False
        return result

    @staticmethod
    def save_to_mongo(file,mongo_model):
        result = ["0","文件大小不能超过10M"]
        if BusinessService.validate_upload_file(file, 10 * 1024 * 1024, None):
            mongo_id = MongoDBService.save_file(file, mongo_model)
            result[0] = mongo_id
        return result


    class ActionLogType(object):
        CI=1



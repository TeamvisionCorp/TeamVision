#coding=utf-8
'''
Created on 2014-11-2

@author: Zhangtiande
'''
from gatesidelib.emailhelper import EmailHelper
from teamvision.settings import EMAILCONFIG
from business.business_service import BusinessService


class EmailService(BusinessService):
    '''
    Email Service for doraemon
    '''
    HOST=EMAILCONFIG['HOST']
    PORT=EMAILCONFIG['PORT']
    USER=EMAILCONFIG['USER']
    PASSWORD=EMAILCONFIG['PASSWORD']
    ISAUTH=EMAILCONFIG['ISAUTH']
    STARTSSL=EMAILCONFIG['STARTSSL']
    POSTFIX=EMAILCONFIG['POSTFIX']
    
    
    @staticmethod
    def sendemail(emailconfig, emaillist, emailmessage, subject):
        emailSender = EmailHelper(BusinessService.HOST,BusinessService.USER,BusinessService.PASSWORD,BusinessService.POSTFIX,BusinessService.PORT)
        message = emailSender.generatetextmessage(emailmessage, subject, ','.join(emaillist), 'html')
        if BusinessService.ISAUTH:
            emailSender.sendemaillogin(emaillist, subject, message.as_string())
        else:
            emailSender.sendmail_nologin(emaillist, subject, message.as_string())
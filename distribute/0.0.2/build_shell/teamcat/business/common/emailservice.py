#coding=utf-8
'''
Created on 2014-11-2

@author: Zhangtiande
'''
from gatesidelib.emailhelper import EmailHelper
from doraemon.settings import EMAILCONFIG
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
        emailSender = EmailHelper(EmailService.HOST,EmailService.USER,EmailService.PASSWORD,EmailService.POSTFIX,EmailService.PORT)
        for reciver in emaillist:
            index = 1
            message = emailSender.generatetextmessage(emailmessage, subject, ','.join(emaillist), 'html')
            if EmailService.ISAUTH:
                emailSender.sendemaillogin(','.join(emaillist), subject, message.as_string())
            else:
                emailSender.sendmail_nologin(','.join(emaillist), subject, message.as_string())
            emaillist = emaillist[index:]
            emaillist.append(reciver)
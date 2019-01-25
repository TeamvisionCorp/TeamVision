#coding=utf-8
'''
Created on 2016-1-18

@author: Devuser
'''

from django import template
from teamvision.auth_extend.user.templatetags import project_role_required_node
from gatesidelib.common.simplelogger import SimpleLogger
from email._header_value_parser import Parameter

register = template.Library()



@register.tag()
def project_tester_required(parser, token):
    parameters=token.split_contents()
    try:
        nodelist = parser.parse(('end_project_tester',))
        parser.delete_first_token()
    except Exception as ex:
        SimpleLogger.exception(ex)
    return project_role_required_node.TesterRequiredNode(nodelist,parameters[1])

@register.tag()
def project_developer_required(parser, token):
    parameters=token.split_contents()
    project_id=0
    try:
        nodelist = parser.parse(('end_project_developer',))
        parser.delete_first_token()
    except Exception as ex:
        SimpleLogger.exception(ex)
    return project_role_required_node.DevRequiredNode(nodelist,parameters[1])

@register.tag()
def project_admin_required(parser, token):
    parameters=token.split_contents()
    project_id=0
    try:
        nodelist = parser.parse(('end_project_admin',))
        parser.delete_first_token()
    except Exception as ex:
        SimpleLogger.exception(ex)
    return project_role_required_node.AdminRequiredNode(nodelist,parameters[1])

@register.tag()
def project_owner_required(parser, token):
    parameters=token.split_contents()
    project_id=0
    try:
        if len(parameters)>1:
            project_id=int(parameters[1])
        nodelist = parser.parse(('end_project_owner',))
        parser.delete_first_token()
    except Exception as ex:
        SimpleLogger.exception(ex)
    return project_role_required_node.OwnerRequiredNode(nodelist,parameters[1])

@register.tag()
def project_manager_required(parser,token):
    parameters=token.split_contents()
    project_id=0
    try:
        nodelist = parser.parse(('end_project_manager',))
        parser.delete_first_token()
    except Exception as ex:
        SimpleLogger.exception(ex)
    return project_role_required_node.ManagerRequiredNode(nodelist,parameters[1])

@register.tag()
def project_user_not_allowed(parser, token):
    parameters=token.split_contents()
    project_id=0
    try:
        nodelist = parser.parse(('end_project_user_not_allowed',))
        parser.delete_first_token()
    except Exception as ex:
        SimpleLogger.exception(ex)
    return project_role_required_node.UserNotAllowedNode(nodelist,parameters[1])
#coding=utf-8
'''
Created on 2016-1-18

@author: Devuser
'''

from django import template
from doraemon.auth_extend.user.templatetags.auth_required_node import LogoutRequiredNode,LoginRequiredNode,UserRequiredNode,ManagerRequiredNode,AdminRequiredNode

register = template.Library()



@register.tag()
def admin_required(parser, token):
    nodelist = parser.parse(('end_admin',))
    parser.delete_first_token()
    return AdminRequiredNode(nodelist)

@register.tag()
def manager_required(parser, token):
    nodelist = parser.parse(('end_manager',))
    parser.delete_first_token()
    return ManagerRequiredNode(nodelist)

@register.tag()
def user_required(parser, token):
    nodelist = parser.parse(('end_user',))
    parser.delete_first_token()
    return UserRequiredNode(nodelist)

@register.tag()
def login_required(parser, token):
    nodelist = parser.parse(('end_login',))
    parser.delete_first_token()
    return LoginRequiredNode(nodelist)

@register.tag()
def logout_required(parser, token):
    nodelist = parser.parse(('end_logout',))
    parser.delete_first_token()
    return LogoutRequiredNode(nodelist)
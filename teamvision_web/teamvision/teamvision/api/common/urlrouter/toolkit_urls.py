#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from django.conf.urls import url
from teamvision.api.common.views import toolkit_view


toolkit_router =[url(r"toolkit/qrcode",toolkit_view.QRCodeView.as_view())]

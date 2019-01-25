#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from doraemon.productquality.views.bugreportview import index_list,load_chartcontainer,load_leftcontainer,get_productname_control,get_productversion
from doraemon.productquality.views.bugreportview import get_perday_bugcounts_data,get_allday_bugcounts_data



urlpatterns = patterns(
                       r'bugreport',url(r"index",index_list),
                       url("loadleftcontainer",load_leftcontainer),
                       url("getproductnamecontrol",get_productname_control),
                       url("getproductversion",get_productversion),
                       url("getchart",load_chartcontainer),
                       url('getbugcountsperday',get_perday_bugcounts_data),
                       url('getalldaybugcounts',get_allday_bugcounts_data),
                       )

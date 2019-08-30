#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import patterns,url
from teamvision.productquality.views.codequalityview import index_list,get_chart,load_leftcontainer,get_productname_control,get_productversion,get_productbugs,get_productbug_rates
from teamvision.productquality.views.codequalityview import get_productcodelines,get_productbug_rates



urlpatterns = patterns(
                       r'codequality',url(r"index",index_list),
                       url("getchart",get_chart),
                       url("loadleftcontainer",load_leftcontainer),
                       url("getproductnamecontrol",get_productname_control),
                       url("getproductversioncontrol",get_productversion),
                       url("getproductbugs",get_productbugs),
                       url("getproductbugrates",get_productbug_rates),
                       url("getcodelines",get_productcodelines)
                       )

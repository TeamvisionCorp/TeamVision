#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CaseTag
# from doraemon.api.ci.filters.ci_pagination import CIPagination
from teamvision.api.ci.filters.case_tag_filter import CaseTagFilterSet


class CaseTagView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.CICaseTagSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        result_id =int(self.kwargs['id'])
        return CaseTag.objects.get(result_id)



class CaseTagListView(generics.ListCreateAPIView):
    """
    /api/ci/case_tags?id__in=1,2: return tag with id 1 and 2
    /api/ci/case_tags return all
    """
    serializer_class = ci_serializer.CICaseTagSerializer
    permission_classes=[AllowAny]
    queryset=CaseTag.objects.all()
    
    def get_queryset(self):
        qs = super(CaseTagListView, self).get_queryset()
        return CaseTagFilterSet(data=self.request.GET, queryset=qs).filter()
    




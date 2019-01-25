#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.ci.serializer import autotesting_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import AutoCase
# from business.ci.ci_task_history_service import CITaskHistoryService
# from rest_framework.response import Response
from teamvision.api.ci.filters.ci_pagination import CIPagination
from teamvision.api.ci.filters.auto_case_filter import AutoCaseFilterSet




CaseTag={'1':'ALL','2':'EC','3':'MF','4':'BVT'}

class AutoCaseView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = autotesting_serializer.AutoCaseSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        result_id =int(self.kwargs['id'])
        return AutoCase.objects.get(result_id)



class AutoCaseListView(generics.ListCreateAPIView):
    """
    /api/ci/auto_cases?ProjectID=1446: return case with ProjectID 1446
    /api/ci/auto_cases?id__in=1,2: return case with id 1 and 2
    /api/ci/auto_cases return all
    """
    serializer_class = autotesting_serializer.AutoCaseSerializer
    permission_classes=[AllowAny]
    queryset=AutoCase.objects.all().filter(IsActive=1)
    pagination_class = CIPagination
    
    def get_queryset(self):
        qs = super(AutoCaseListView, self).get_queryset().filter(IsActive=1)
        case_tags=self.request.GET.get('CaseTag',None)
        case_subset=list()
        if case_tags and not '1' in case_tags:
            if not ',' in case_tags:
                case_tags=case_tags+","
            for tag in eval(case_tags):
                result=qs.filter(CaseTag__contains=CaseTag[str(tag)])
                case_subset.append(result)
            for subset in case_subset:
                result=result|subset
            qs=result.distinct()
        return AutoCaseFilterSet(data=self.request.GET, queryset=qs).filter()
    




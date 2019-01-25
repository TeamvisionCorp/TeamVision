#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from business.business_service import BusinessService
from teamvision.ci.models import AutoCaseResult,AutoTestingTaskResult,UnitTestCaseResult
from teamvision.ci.viewmodels.vm_auto_case_result import VM_AutoCaseResult
from gatesidelib.common.simplelogger import SimpleLogger
from business.common.excel_file_service import ExcelFileService
import xlwt



class CITestingHistoryService(BusinessService,ExcelFileService):
    '''
    classdocs
    '''
    
    @staticmethod
    def case_result_excel_file(history_id):
        print(history_id)
        wb = xlwt.Workbook(encoding='utf-8')
        sheet_all = wb.add_sheet('ALL')
        sheet_success = wb.add_sheet('Success')
        sheet_fail = wb.add_sheet('Fail')
        sheet_aborted = wb.add_sheet('Aborted')
        sheet_all=CITestingHistoryService.case_result_sheet(sheet_all, history_id,0," 32")
        sheet_success=CITestingHistoryService.case_result_sheet(sheet_success, history_id,3," 3")
        sheet_fail=CITestingHistoryService.case_result_sheet(sheet_fail, history_id,2," 2")
        sheet_aborted=CITestingHistoryService.case_result_sheet(sheet_aborted, history_id,1," 47")
        return wb
    
    @staticmethod
    def case_result_sheet(excel_sheet,history_id,result_type,sheet_type):
        task_result=AutoTestingTaskResult.objects.get_by_historyid(history_id)
        auto_case_results=list()
        if task_result:
            auto_case_results=AutoCaseResult.objects.get_by_resultid(task_result.id,result_type)
            if len(auto_case_results)==0:
                auto_case_results=UnitTestCaseResult.objects.get_by_task_result(task_result.id,result_type)
        vm_case_results=list()
        for case_result in auto_case_results:
            temp_case_result=VM_AutoCaseResult(case_result)
            vm_case_results.append(temp_case_result)
        excel_sheet=CITestingHistoryService.get_case_result_sheet(excel_sheet,vm_case_results,sheet_type)
        return excel_sheet
    
    @staticmethod
    def get_case_result_sheet(excel_sheet,result_list,sheet_type):
        style_heading=CITestingHistoryService.get_heading_style(sheet_type)
        style_body=CITestingHistoryService.get_style_body()
#         style_body.num_format_str =CITestingHistoryService.get_body_formats()[0]
        excel_sheet=CITestingHistoryService.get_sheet_header(excel_sheet, style_heading)
        excel_sheet=CITestingHistoryService.get_sheet_body(result_list, excel_sheet,style_body)
        return excel_sheet
    
    @staticmethod
    def get_sheet_header(excle_sheet,heading_style):
        excle_sheet.write(0, 0, '用例ID', heading_style)
        excle_sheet.write(0, 1, '用例名称', heading_style)
        excle_sheet.write(0, 2, '持续时间', heading_style)
        excle_sheet.write(0, 3, '执行设备', heading_style)
        excle_sheet.write(0, 4, '错误信息', heading_style)
        excle_sheet.write(0, 5, '详细信息', heading_style)
        return excle_sheet
    
    @staticmethod
    def get_sheet_body(result_list,excel_sheet,body_style):
        row = 1
        case_id_style=CITestingHistoryService.get_column_style('32')
        for result in result_list:
            if result.auto_case_result.Result==3:
                case_id_style=CITestingHistoryService.get_column_style('3')
            if result.auto_case_result.Result==2:
                case_id_style=CITestingHistoryService.get_column_style('2')
            if result.auto_case_result.Result==1:
                case_id_style=CITestingHistoryService.get_column_style('1')
            excel_sheet.write(row, 0, result.auto_case_result.TestCaseID,case_id_style)
            excel_sheet.write(row, 1, result.case_name(), body_style)
            excel_sheet.write(row, 2, result.duration,body_style)
            excel_sheet.write(row, 3, result.device_name(),body_style)
            excel_sheet.write(row, 4, result.auto_case_result.Error, body_style)
            excel_sheet.write(row, 5, result.auto_case_result.StackTrace, body_style)

        # 第一行加宽
            excel_sheet.col(0).width = 100 * 50
            excel_sheet.col(1).width = 200 * 50
            excel_sheet.col(2).width = 100 * 50
            excel_sheet.col(3).width = 100 * 50
            excel_sheet.col(4).width = 200 * 50
            excel_sheet.col(5).width = 300 * 50
            row += 1
        return excel_sheet
        
        
    
    


    
    

        
        
        
        
        
        
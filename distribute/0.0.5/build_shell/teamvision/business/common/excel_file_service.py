# coding=utf-8
'''
Created on 2018年4月12日

@author: zhangtiande
'''

import xlwt

class ExcelFileService(object):
    '''
    classdocs
    '''
     
    @staticmethod
    def get_heading_style(sheet_type):
        style_heading = xlwt.easyxf("""
        font:
            name Arial,
            colour_index white,
            bold on,
            height 360;
        align:
            wrap off,
            vert center,
            horiz center;
        pattern:
            pattern solid,
            fore-colour"""+sheet_type+""";
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """)
        return style_heading
    
    @staticmethod
    def get_style_body():
        style_body = xlwt.easyxf("""
        font:
            name Arial,
            bold off,
            height 300;
        align:
            wrap on,
            vert center,
            horiz left;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """)
        return style_body
    

    
    @staticmethod
    def get_column_style(color):
        style_red = xlwt.easyxf("""
        font:
            name Arial,
            bold off,
            colour_index """+color+""",
            height 300;
        align:
            wrap on,
            vert center,
            horiz left;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """)
        return style_red
    
    @staticmethod
    def get_body_formats():
        fmts = [
        'M/D/YY',
        'D-MMM-YY',
        'D-MMM',
        'MMM-YY',
        'h:mm AM/PM',
        'h:mm:ss AM/PM',
        'h:mm',
        'h:mm:ss',
        'M/D/YY h:mm',
        'mm:ss',
        '[h]:mm:ss',
        'mm:ss.0',
        ]
        return fmts
    
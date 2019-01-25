#coding=utf-8
'''
Created on 2016-12-2

@author: Administrator
'''

import qrcode
from io import BytesIO
from PIL import Image

class QRCodeHelper(object):
    '''
    classdocs
    '''


    @staticmethod
    def save_code_image(content,filepath):
        qr=qrcode.QRCode(
        version=4,  #生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%
        box_size=10, #每个格子的像素大小
        border=2, #边框的格子宽度大小
        )
        qr.add_data(content)
        qr.make(fit=True) 
        img=qr.make_image()
        img.save(filepath)
    
    @staticmethod
    def save_qr_code_stream(content):
        qr=qrcode.QRCode(
        version=4,  #生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%
        box_size=10, #每个格子的像素大小
        border=2, #边框的格子宽度大小
        )
        qr.add_data(content)
        qr.make(fit=True) 
#         img = qr.make(content)
        buf = BytesIO()
        img=qr.make_image()
        img.save(buf)
        image_stream = buf.getvalue()
        return image_stream
        
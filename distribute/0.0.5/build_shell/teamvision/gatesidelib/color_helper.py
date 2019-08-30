# coding=utf-8
'''
Created on 2018年1月30日

@author: ethan
'''
import random

class ColorHelper(object):
    '''
    classdocs
    '''
    @staticmethod
    def rgb2hex(rgb_color_array):
        output = "#"
        for x in rgb_color_array: 
            intx = int(x)
            if intx < 16:
                output = output + '0' + hex(intx)[-2:]
            else:
                output = output + hex(intx)[-2:] 
        return output

    @staticmethod
    def random_color():
        rgb_color_array=list()
        rgb_color_array.append(random.randint(0,255))
        rgb_color_array.append(random.randint(0,255))
        rgb_color_array.append(random.randint(0,255))
        return ColorHelper.rgb2hex(rgb_color_array)
        
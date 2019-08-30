#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: zhangtiande
'''

class VM_Product(object):
    '''
    MyPlace business model
    '''
    
    def __init__(self,loginuser,product,selected_product):

        self.user=loginuser
        self.product=product
        self.selected_product=selected_product
    
    
    def is_selected(self):
        if self.product.id==self.selected_product:
            return "selected"
            
            
        
            
        
        
            
        
        
        
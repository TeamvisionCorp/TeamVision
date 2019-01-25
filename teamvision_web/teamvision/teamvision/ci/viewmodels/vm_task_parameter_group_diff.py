#coding=utf-8
'''
Created on 2017年4月26日

@author: ethan
'''

class VM_TaskParameterGroupDiff(object):
    '''
    classdocs
    '''


    def __init__(self,saved_object,changed_object):
        '''
        Constructor
        '''
        self.save_object=saved_object
        self.changed_object=changed_object
    
    def parameter_group_property_diff(self):
        result=list()
        if self.save_object.group_name!=self.changed_object.group_name:
            temp=ParameterGroupDiff()
            temp.field_name="Group Name"
            temp.field_old_value=self.save_object.group_name
            temp.field_new_value=self.changed_object.group_name
            result.append(temp)
        if self.save_object.description!=self.changed_object.description:
            temp=ParameterGroupDiff()
            temp.field_name="Description"
            temp.field_old_value=self.save_object.description
            temp.field_new_value=self.changed_object.description
            result.append(temp)
        if self.save_object.is_default!=self.changed_object.is_default:
            temp=ParameterGroupDiff()
            temp.field_name="Default"
            temp.field_old_value=self.save_object.is_default
            temp.field_new_value=self.changed_object.is_default
            result.append(temp)
        
        return result;
    
    
    def parameter_diff(self):
        result=list()
        if self.save_object.parameters==None:
            return result
        for o_parameter in self.save_object.parameters:
            for c_parameter in self.changed_object.parameters:
                if o_parameter.key==c_parameter.key:
                    if o_parameter.value!=c_parameter.value:
                        temp=ParameterGroupDiff()
                        temp.field_name=o_parameter.key
                        temp.field_old_value=o_parameter.value
                        temp.field_new_value=c_parameter.value
                        result.append(temp)
                        break
        return result
                          
    
    def parameter_delete(self):
        result=list()
        if self.save_object.parameters==None:
            return result
        for o_parameter in self.save_object.parameters:
            flag=False
            for c_parameter in self.changed_object.parameters:
                if o_parameter.key==c_parameter.key:
                    flag=True
                    break
            if not flag:
                temp=ParameterGroupDiff()
                temp.field_name=o_parameter.key
                temp.field_old_value=o_parameter.value
                result.append(temp)
        return result
                
    
    def parameter_new(self):
        result=list()
        if self.changed_object.parameters==None:
            return result
        for c_parameter in self.changed_object.parameters:
            flag=True
            if self.save_object.parameters:
                for o_parameter in self.save_object.parameters:
                    if o_parameter.key==c_parameter.key:
                        flag=False
                        break
                    else:
                        flag=True
            if flag:
                temp=ParameterGroupDiff()
                temp.field_name=c_parameter.key
                temp.field_new_value=c_parameter.value
                result.append(temp)
        return result
    
    
    
class ParameterGroupDiff(object):
    field_name=""
    field_old_value=""
    field_new_value=""    

        
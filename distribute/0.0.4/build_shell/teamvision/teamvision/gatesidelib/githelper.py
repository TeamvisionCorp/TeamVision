#coding=utf-8
#coding=utf-8
'''
Created on 2014-12-16

@author: Devuser
'''

import os
from gatesidelib.filehelper import FileHelper
from gatesidelib.common.simplelogger import SimpleLogger

class GitHelper(object):
    '''
    git command helper
    '''
    git_clonecommand="git clone -b {BRANCHNAME} {REPERTORY} {PROJECTPATH} >> "
    git_pullcommand="git  --git-dir={PROJECTPATH} pull {REPERTORY} >> "
    git_logcommand="git --git-dir={PROJECTPATH} log {REVERSIONRANGE} >> "
    git_diffcommand="git --git-dir={PROJECTPATH} diff {STARTVERSION} {ENDVERSION} --stat >> "

    def __init__(self,giturl,projectpath,logfilepath):
        '''
        giturl: git repertory address
        username: username for git repretory
        password: password for git repertory
        '''
        self.project=projectpath
        self.url=giturl
        self.templog=logfilepath
    
    def get_changecode_lines(self,startversion,endversion):
        gitcommandtext=self.get_gitcommand(GitHelper.git_diffcommand, startversion, endversion,"","")
        os.popen(gitcommandtext)
        linecounts=self.get_linecounts(self.templog)
        return linecounts
    

    def clone_project(self,branchname):
        if os.path.exists(self.project):
            FileHelper.delete_dir_all(self.project)
        gitcommandtext=self.get_gitcommand(GitHelper.git_clonecommand,"","","",branchname)
        SimpleLogger.info(gitcommandtext)
        os.popen(gitcommandtext)
    
    def pull_project(self):
        gitcommandtext=self.get_gitcommand(GitHelper.git_pullcommand,"","","","")
        SimpleLogger.info(gitcommandtext)
        os.popen(gitcommandtext)
        
    
    def get_commitlog(self,reversionNumber):
        gitcommandtext=self.get_gitcommand(GitHelper.git_logcommand,"","",reversionNumber,"")
        FileHelper.delete_file(self.templog)
        os.popen(gitcommandtext)
        return FileHelper.read_lines(self.templog)
    
    def save_commitlog(self,reversionNumber):
        gitcommandtext=self.get_gitcommand(GitHelper.git_logcommand,"","",reversionNumber,"")
        FileHelper.delete_file(self.templog)
        os.popen(gitcommandtext)
    
    
    def get_allcodelines(self,startversion,endversion):
        gitcommandtext=self.get_gitcommand(GitHelper.git_diffcommand,startversion,endversion,"","")
        FileHelper.delete_file(self.templog)
        os.popen(gitcommandtext)
        linecounts=FileHelper.get_linecounts(self.templog)
        return linecounts
        
    
    def get_gitcommand(self,command,startversion,endversion,versionNumber,branchname):
        commandtext=command.replace("{STARTVERSION}",startversion)
        commandtext=commandtext.replace("{ENDVERSION}",endversion)
        commandtext=commandtext.replace("{REPERTORY}",self.url)
        commandtext=commandtext.replace("{PROJECTPATH}",self.project)
        commandtext=commandtext.replace("{REVERSIONRANGE}",versionNumber)
        commandtext=commandtext.replace("{BRANCHNAME}",branchname)
        return commandtext+self.templog
    
    
    def get_linecounts(self,filename):
        filehandler=open(filename,'r')
        linelist=[line for line in filehandler]
        linelist.reverse()
        if linelist[0]:
            if "," in linelist[0]:
                changeinfos=linelist[0].split(',')
                if len(changeinfos)==2:
                    new_codeline_counts=self.get_number_from_string(changeinfos[1])
                    deleted_codeline_counts=0
                if len(changeinfos)==3:
                    new_codeline_counts=self.get_number_from_string(changeinfos[1])
                    deleted_codeline_counts=self.get_number_from_string(changeinfos[2])
            else:
                new_codeline_counts=0
                deleted_codeline_counts=0
        return [new_codeline_counts,deleted_codeline_counts]
    
    def get_number_from_string(self,str_contains_num):
        tempstr=str_contains_num.strip()
        number=""
        for char in tempstr:
            if char.isdigit():
                number=number+char
        return number
        
        
        
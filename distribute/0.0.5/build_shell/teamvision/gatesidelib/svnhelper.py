#coding=utf-8
#coding=utf-8
'''
Created on 2014-12-10

@author: Devuser
'''

import os
from gatesidelib.filehelper import FileHelper
from gatesidelib.common.simplelogger import SimpleLogger

class SvnHelper(object):
    '''
    Svn 相关信息
    '''
    svn_logcommand="svn log -r {STARTVERSION}:{ENDVERSION}  {URL} --username {USER} --password {PASSWORD} >> "
    svn_diffcommand="svn diff -r{STARTVERSION}{ENDVERSION} {URL} --username {USER} --password {PASSWORD} >> "
    local_svn_dir="  --config-dir /web/www/.subversion"
    no_store_password="   --no-auth-cache"

    def __init__(self,svnurl,username,password,templogfilepath):
        self.user=username
        self.url='\''+svnurl+'\''
        self.passwd=password
        self.templog=templogfilepath

    def get_newcode_lines(self,startversion,endversion):
        if startversion=='0':
            startversion=endversion
            endversion=''
        else:
            startversion=startversion+':'
        svncommandtext=self.get_svncommand(SvnHelper.svn_diffcommand, startversion, endversion)
        os.system(svncommandtext)
        linecounts=self.get_linecounts(self.templog,'+')
        return linecounts
    
    def get_deletecode_lines(self,startversion,endversion):
        if startversion=='0':
            startversion=endversion
            endversion=''
        else:
            startversion=startversion+':'
        svncommandtext=self.get_svncommand(SvnHelper.svn_diffcommand, startversion, endversion)
        os.popen(svncommandtext)
        linecounts=self.get_linecounts(self.templog,'-')
        return linecounts
    
    def get_commitlog(self,startversion,endversion):
        svncommandtext=self.get_svncommand(SvnHelper.svn_logcommand, startversion, endversion)
        FileHelper.delete_file(self.templog)
        os.popen(svncommandtext)
        return FileHelper.read_lines(self.templog)
    
    def save_commitlog(self,startversion,endversion):
        svncommandtext=self.get_svncommand(SvnHelper.svn_logcommand, startversion, endversion)
        FileHelper.delete_file(self.templog)
        os.popen(svncommandtext)
    
    
    def get_allcodelines(self,reversion):
        svncommandtext=self.get_svncommand(SvnHelper.svn_diffcommand, '0',reversion)
        FileHelper.delete_file(self.templog)
        os.popen(svncommandtext)
        linecounts=FileHelper.get_linecounts(self.templog)
        return linecounts
        
    
    def get_svncommand(self,command,startversion,endversion):
        commandtext=command.replace("{STARTVERSION}",startversion)
        commandtext=commandtext.replace("{ENDVERSION}",endversion)
        commandtext=commandtext.replace("{URL}",self.url)
        commandtext=commandtext.replace("{USER}",self.user)
        commandtext=commandtext.replace("{PASSWORD}",self.passwd)
        SimpleLogger.info(commandtext+self.templog+SvnHelper.local_svn_dir+SvnHelper.no_store_password)
        return commandtext+self.templog+SvnHelper.local_svn_dir+SvnHelper.no_store_password
    
    def get_linecounts(self,filename,symbol):
        count=0
        filehandler=open(filename,'r')
        for line in filehandler:
            if line.startswith(symbol):
                count=count+1
        return count
        
#coding=utf-8
#encoding=utf-8
'''
Created on 2014-12-17

@author: zhangtiande
'''
from dataaccess.testjob.dal_testjob import DAL_TestJob
from dataaccess.testjob.dal_testproject import DAL_TestProject
from dataaccess.testjob.dal_testsubmition import DAL_TestSubmition
from gatesidelib.svnhelper import SvnHelper
from gatesidelib.githelper import GitHelper
from doraemon.testjob.datamodels.scminfo import SCMInfo
from dataaccess.common.dal_dictvalue import DAL_DictValue
from dataaccess.testjob.dal_codecommitlog import DAL_CodeCommitLog
from doraemon.testjob.models import CodeCommitLog
from gatesidelib.common.simplelogger import SimpleLogger
from gatesidelib.filehelper import FileHelper
from gatesidelib.common.commonhelper import CommonHelper
import time,datetime
import os


class CodeCommitLogService(object):
    '''
               代码提交日志服务
    '''
    
    @staticmethod
    def update_commit_log(testjobid):
        testjob= DAL_TestJob.gettestjob(testjobid)
        if int(testjob.TJProgress)==100 and (testjob.TJCodeLines==0):
            SimpleLogger.logger.info("start to get commit log for job:"+ str(testjobid))
            CodeCommitLogService.update_svn_commit_log(testjob.TJSubmitionID)
            CodeCommitLogService.update_git_commit_log(testjob.TJSubmitionID)
            CodeCommitLogService.update_tesjob_codelines(testjobid)
            SimpleLogger.logger.info("finished to get commit log for job:"+ str(testjobid))
    
    @staticmethod
    def update_tesjob_codelines(testjobid):
        SimpleLogger.logger.info("start to update codelines for job:"+ str(testjobid))
        testjob= DAL_TestJob.gettestjob(testjobid)
        codeCommitLogs=DAL_CodeCommitLog.get_commitlogs_by_submitionid(testjob.TJSubmitionID)
        codeLines=0
        for codeCommitLog in codeCommitLogs:
            if not CodeCommitLogService.is_codecomite_expire(codeCommitLog.CCLCommiteDate):
                tempcodelines=int(codeCommitLog.CCLNewCodeLines)
                if tempcodelines>30000:
                    codeLines=codeLines+tempcodelines*0.1
                elif tempcodelines<=30000 and tempcodelines>10000:
                    codeLines=codeLines+tempcodelines*0.2
                else:
                    codeLines=codeLines+tempcodelines       
        testjob.TJCodeLines=codeLines
        DAL_TestJob.updatetestjob(testjob)
        SimpleLogger.logger.info("finished to update codelines for job:"+ str(testjobid))
    
    @staticmethod
    def is_codecomite_expire(codecommitdate):
        if codecommitdate:
            commitdate_string=codecommitdate.split('+')[0].strip() #获取+号前的部分时间字符串
            try:
                commitdate_time=time.strptime(commitdate_string,'%a %b %d %H:%M:%S %Y') #git log 提交日期转化成time格式
            except Exception as ex:
                commitdate_time=time.strptime(commitdate_string,'%Y-%m-%d %H:%M:%S') #git log 提交日期转化成time格式
            commitdate=datetime.date(commitdate_time.tm_year,commitdate_time.tm_mon,commitdate_time.tm_mday) #转化成日期格式
            intervals=(datetime.date.today()-commitdate).days
            if intervals>90:
                SimpleLogger.logger.info("code submit date expire")
                return True
            else:
                return False
        
    @staticmethod
    def get_commit_log(submitionid):
        pass

    
    @staticmethod
    def update_svn_commit_log(submitionid):
        SimpleLogger.logger.info("start to process  svn commit log for submition:"+ str(submitionid))
        testsubmition=DAL_TestSubmition.gettestsubmition(submitionid)
        if testsubmition.TPSCodeVersion!=None and testsubmition.TPSCodeVersion.isdigit():
            log_file_path=CodeCommitLogService.save_svn_commit_log(testsubmition)
            CodeCommitLogService.save_svn_commitlog_2DB(log_file_path, testsubmition)
            FileHelper.delete_file(log_file_path)
            SimpleLogger.logger.info("finished to process  svn commit log for submition:"+ str(submitionid))
              
    @staticmethod
    def update_git_commit_log(submitionid):
        SimpleLogger.logger.info("start to process  git commit log for submition:"+ str(submitionid))
        testsubmition=DAL_TestSubmition.gettestsubmition(submitionid)
        if testsubmition.TPSCodeVersion!=None and not testsubmition.TPSCodeVersion.isdigit():
            CodeCommitLogService.clone_git_project(testsubmition)
#             CodeCommitLogService.pull_git_project(testsubmition)
            log_file_path=CodeCommitLogService.save_git_commit_log(testsubmition)
            SimpleLogger.logger.info(log_file_path)
            CodeCommitLogService.save_git_commitlog_2DB(log_file_path, testsubmition)
            FileHelper.delete_file(log_file_path)
            
    
    
    @staticmethod
    def save_svn_commitlog_2DB(logfilepath,testsubmition):
        SimpleLogger.logger.info("start to save svn info to db for submition:"+ str(testsubmition.id))
        SimpleLogger.logger.info("logfilepaht"+logfilepath)
        if os.path.isfile(logfilepath):
            SimpleLogger.logger.info("logfile exits")
            commitlog=open(logfilepath,'r')
            last_commitnumber=CodeCommitLogService.get_lastest_svncommit_number(testsubmition.TPSProductName,testsubmition.id)
            SimpleLogger.logger.info(last_commitnumber)
            linesets=list()
            for line in commitlog:
                templine=str(line)
                try:
                    if len(linesets) and templine.startswith('----'):
                        SimpleLogger.logger.info(templine)
                        code_commit_log= CodeCommitLogService.init_svncommitlog(linesets,last_commitnumber,testsubmition)
                        if DAL_CodeCommitLog.get_commitlog_by_commitnumber(code_commit_log.CCLCommiteNumber):
                            SimpleLogger.logger.info(code_commit_log.CCLCommiteNumber)
                            pass
                        else:
                            if code_commit_log.CCLCommiteNumber==testsubmition.TPSCodeVersion:
                                SimpleLogger.logger.info(code_commit_log.CCLCommiteNumber)
                                DAL_CodeCommitLog.save_commitlog(code_commit_log)
                                break;
                            else:
                                SimpleLogger.logger.info("no exits version")
                                DAL_CodeCommitLog.save_commitlog(code_commit_log)
                                last_commitnumber=code_commit_log.CCLCommiteNumber
                                linesets=list()
                                linesets.append(templine)
                    else:
                        linesets.append(templine)
                except Exception as ex:
                    SimpleLogger.logger.error(ex)
                    continue
        SimpleLogger.logger.info("finished to save svn info to db for submition:"+ str(testsubmition.id))
                
    @staticmethod
    def save_git_commitlog_2DB(logfilepath,testsubmition):
        linesets=CodeCommitLogService.process_git_commitlog(logfilepath)
        linesets.reverse()
        last_commitnumber=CodeCommitLogService.get_lastest_gitcommit_number(testsubmition.TPSProductName,testsubmition.id)
        if last_commitnumber=="0":
            last_commitnumber=""
        for linelist in linesets:
            try:
                code_commit_log= CodeCommitLogService.init_gitcommitlog(linelist, last_commitnumber, testsubmition)
                if DAL_CodeCommitLog.get_commitlog_by_commitnumber(code_commit_log.CCLCommiteNumber): # 已经存在的条目不再写入
                    pass
                else:
                    if code_commit_log.CCLCommiteNumber==testsubmition.TPSCodeVersion:
                        DAL_CodeCommitLog.save_commitlog(code_commit_log)
                        break;
                    else:
                        SimpleLogger.logger.info("no exists commit version:"+code_commit_log.CCLCommiteNumber)
                        DAL_CodeCommitLog.save_commitlog(code_commit_log)
                        last_commitnumber=code_commit_log.CCLCommiteNumber
            except Exception as ex:
                SimpleLogger.logger.error(ex)
                continue
            
    
    @staticmethod
    def init_gitcommitlog(linelist,startrevision,testsubmition):
        code_commit_log=CodeCommitLog()
        code_commit_log=CodeCommitLogService.extract_gitcommitlog(linelist, code_commit_log)
        commitloglines=[linelist[i] for i in range(len(linelist)) if i>3]
        code_commit_log.CCLCommiteLog=str(commitloglines).decode('gb2312')[0:10000]
        codelinecounts=CodeCommitLogService.get_git_line_counts(testsubmition,startrevision,code_commit_log.CCLCommiteNumber)
        code_commit_log.CCLNewCodeLines=int(codelinecounts[0])
        code_commit_log.CCLDeletedCodeLines=int(codelinecounts[1])
        code_commit_log.CCLProductID=testsubmition.TPSProductName
        code_commit_log.CCLProductVersion=testsubmition.TPSProductVersion
        code_commit_log.CCLSubmitionID=testsubmition.id
        return code_commit_log
            
    
    @staticmethod
    def process_git_commitlog(logfilepath):
        if os.path.isfile(logfilepath):
            commitlog=open(logfilepath,'r')
            templinesets=list()
            linesets=list()
            for line in commitlog:
                templine=str(line)
                try:
                    if len(templinesets) and templine.startswith('commit'):
                        linesets.append(templinesets)
                        templinesets=list()
                        templinesets.append(templine)
                    else:
                        templinesets.append(templine)
                except Exception as ex:
                    SimpleLogger.logger.error(ex)
                    continue
        return linesets
    
               
    @staticmethod
    def init_svncommitlog(linelist,startrevision,testsubmition):
        code_commit_log=CodeCommitLog()
        code_commit_log=CodeCommitLogService.extract_svncommitlog(linelist[1],code_commit_log)
        commitloglines=[linelist[i] for i in range(len(linelist)) if i>1]
        code_commit_log.CCLCommiteLog=str(commitloglines).decode('gb2312')[0:10000]
        code_commit_log.CCLNewCodeLines=int(CodeCommitLogService.get_svn_line_counts(testsubmition,startrevision,code_commit_log.CCLCommiteNumber,True))
        code_commit_log.CCLDeletedCodeLines=int(CodeCommitLogService.get_svn_line_counts(testsubmition,startrevision,code_commit_log.CCLCommiteNumber,False))
        code_commit_log.CCLProductID=testsubmition.TPSProductName
        code_commit_log.CCLProductVersion=testsubmition.TPSProductVersion
        code_commit_log.CCLSubmitionID=testsubmition.id
        return code_commit_log
    
    @staticmethod
    def extract_svncommitlog(line,code_commit_log):
        logInfos=line.split('|')
        if len(logInfos):
            code_commit_log.CCLCommiteNumber=logInfos[0].replace('r','').strip()
            code_commit_log.CCLCommitor=logInfos[1].strip()
            code_commit_log.CCLCommiteDate=str(logInfos[2].strip()).decode("gb2312")
        return code_commit_log
    
    @staticmethod
    def extract_gitcommitlog(linesets,code_commit_log):
        for line in linesets:
            if str(line).startswith("commit"):
                code_commit_log.CCLCommiteNumber=line.replace('commit','').strip()
            
            if str(line).startswith("Author"):
                code_commit_log.CCLCommitor=line.replace('Author:','').strip()
            
            if str(line).startswith("Date"):
                code_commit_log.CCLCommiteDate=line.replace('Date:','').strip()
        return code_commit_log
            
    
    
    
    @staticmethod
    def save_svn_commit_log(testsubmition):
        SimpleLogger.logger.info("start to save svn commit log for submition:"+ str(testsubmition.id))
        scm_info=CodeCommitLogService.get_svn_scminfo(testsubmition.TPSProductName)
        scm_local_file_path=scm_info.localdir+str(time.time())+".log"
        svn_helper=SvnHelper(testsubmition.TPSCodeUrl,scm_info.scmuser,scm_info.scmpassword,scm_local_file_path)
        last_commit_number=CodeCommitLogService.get_lastest_svncommit_number(testsubmition.TPSProductName,testsubmition.id)
        if last_commit_number!='0':
            last_commit_number=str(int(last_commit_number)+1)
        svn_helper.save_commitlog(last_commit_number,testsubmition.TPSCodeVersion)
        SimpleLogger.logger.info("finished to save svn commit log for submition:"+ str(testsubmition.id))
        return scm_local_file_path
    
    @staticmethod
    def save_git_commit_log(testsubmition):
        scm_info=CodeCommitLogService.get_git_scminfo(testsubmition.TPSProductName)
        scm_local_file_path=scm_info.localdir+CommonHelper.get_slash()+str(time.time())+".log"
        git_url=CodeCommitLogService.generate_git_url(testsubmition.TPSCodeUrl,scm_info.scmuser,scm_info.scmpassword)
        git_helper=GitHelper(git_url,scm_info.localdir+CommonHelper.get_slash()+".git",scm_local_file_path)
#         if CodeCommitLogService.has_gitlog_indb(testsubmition.TPSProductName,testsubmition.id):
#             git_helper.save_commitlog("-200")
#         else:
        git_helper.save_commitlog("")
        return scm_local_file_path
    
    @staticmethod
    def generate_git_url(sourceurl,username,password):
        sourceurllist=sourceurl.split("//")
        return sourceurllist[0]+"//"+username+":"+password+"@"+sourceurllist[1]
    
    @staticmethod
    def clone_git_project(testsubmition):
        SimpleLogger.logger.info("start to clone  git project for submition:"+ str(testsubmition.id))
        scm_info=CodeCommitLogService.get_git_scminfo(testsubmition.TPSProductName)
        scm_local_file_path=scm_info.localdir+str(time.time())+".log"
        codeurlinfo=CodeCommitLogService.get_codeurlinfo(testsubmition.TPSCodeUrl)
        git_url=CodeCommitLogService.generate_git_url(codeurlinfo[0],scm_info.scmuser,scm_info.scmpassword)
        git_helper=GitHelper(git_url,scm_info.localdir,scm_local_file_path)
        git_helper.clone_project(codeurlinfo[1])
        FileHelper.delete_file(scm_local_file_path)
        SimpleLogger.logger.info("finished to clone  git project for submition:"+ str(testsubmition.id))
        
    @staticmethod
    def pull_git_project(testsubmition):
        SimpleLogger.logger.info("start to pull git project for submition:"+ str(testsubmition.id))
        scm_info=CodeCommitLogService.get_git_scminfo(testsubmition.TPSProductName)
        scm_local_file_path=scm_info.localdir+str(time.time())+".log"
        git_url=CodeCommitLogService.generate_git_url(testsubmition.TPSCodeUrl,scm_info.scmuser,scm_info.scmpassword)
        git_helper=GitHelper(git_url+"  master",scm_info.localdir+CommonHelper.get_slash()+".git",scm_local_file_path)
        git_helper.pull_project()
        FileHelper.delete_file(scm_local_file_path)
        
    
    @staticmethod
    def get_svn_line_counts(testsubmition,startrevison,endrevison,is_newcode):
        scm_info=CodeCommitLogService.get_svn_scminfo(testsubmition.TPSProductName)
        scm_local_file_path=scm_info.localdir+str(time.time())+".log"
        svn_helper=SvnHelper(testsubmition.TPSCodeUrl,scm_info.scmuser,scm_info.scmpassword,scm_local_file_path)
        if is_newcode:
            codeline_counts=svn_helper.get_newcode_lines(startrevison,endrevison)
        else:
            codeline_counts=svn_helper.get_deletecode_lines(startrevison,endrevison)
        FileHelper.delete_file(scm_local_file_path)
        return codeline_counts
    
    @staticmethod
    def get_git_line_counts(testsubmition,startrevison,endrevison):
        scm_info=CodeCommitLogService.get_git_scminfo(testsubmition.TPSProductName)
        scm_local_file_path=scm_info.localdir+CommonHelper.get_slash()+str(time.time())+".log"
        git_helper=GitHelper("",scm_info.localdir+CommonHelper.get_slash()+".git",scm_local_file_path)
        codeline_counts= git_helper.get_changecode_lines(startrevison, endrevison)
        FileHelper.delete_file(scm_local_file_path)
        return codeline_counts
    
    @staticmethod
    def has_gitlog_indb(productid,submitionid):
        commitLogSets=DAL_CodeCommitLog.get_commitlog_by_productid(productid)
        target_submition=DAL_TestSubmition.gettestsubmition(submitionid)
        result=False
        for commitlog in commitLogSets:
            tempSubmition=DAL_TestSubmition.gettestsubmition(commitlog.CCLSubmitionID)
            if tempSubmition.TPSPlatform==target_submition.TPSPlatform:
                result=True
                break
        return result
    @staticmethod
    def get_lastest_gitcommit_number(productid,submitionid):
        commitLogSets=DAL_CodeCommitLog.get_commitlog_by_productid(productid)
        target_submition=DAL_TestSubmition.gettestsubmition(submitionid)
        result='0'
        for commitlog in commitLogSets:
            tempSubmition=DAL_TestSubmition.gettestsubmition(commitlog.CCLSubmitionID)
            if tempSubmition.TPSPlatform==target_submition.TPSPlatform:
                if not commitlog.CCLCommiteNumber.isdigit():
                    result=commitlog.CCLCommiteNumber
                    break
        return result
    
    @staticmethod
    def get_lastest_svncommit_number(productid,submitionid):
        commitLogSets=DAL_CodeCommitLog.get_commitlog_by_productid(productid)
        target_submition=DAL_TestSubmition.gettestsubmition(submitionid)
        result='0'
        for commitlog in commitLogSets:
            tempSubmition=DAL_TestSubmition.gettestsubmition(commitlog.CCLSubmitionID)
            if tempSubmition.TPSPlatform==target_submition.TPSPlatform:
                if commitlog.CCLCommiteNumber.isdigit():
                    result=commitlog.CCLCommiteNumber
                    break
        return result
    
    @staticmethod
    def get_svn_scminfo(productnameid):
        return CodeCommitLogService.get_scminfo(productnameid,'SvnUser','SvnPassword','SvnCodeRoot')
    
    @staticmethod
    def get_git_scminfo(productnameid):
        return CodeCommitLogService.get_scminfo(productnameid,'GitUser','GitPassword','GitCodeRoot')
    
    @staticmethod
    def get_scminfo(productnameid,user_dicdataname,password_dicdataname,coderoot_dicdataname):
        scm_user=str(DAL_DictValue.getdatavaluebydataname("SCMInfo",user_dicdataname).DicDataDesc)
        scm_password=str(DAL_DictValue.getdatavaluebydataname("SCMInfo",password_dicdataname).DicDataDesc)
        scm_desc=str(DAL_TestProject.get_testproject(productnameid).TPKEY)
        scm_coderoot=str(DAL_DictValue.getdatavaluebydataname("SCMInfo",coderoot_dicdataname).DicDataDesc)
        scm_info=SCMInfo(scm_user,scm_password,scm_coderoot+CommonHelper.get_slash()+scm_desc)
        return scm_info
    
    @staticmethod
    def get_codeurlinfo(sourceurl):
        print(sourceurl)
        result=list()
        if sourceurl:
            urlinfos=sourceurl.split(":")
            result.append(urlinfos[0]+":"+urlinfos[1].strip())
            if len(urlinfos)<3:
                result.append('master')
            else:
                startindex=urlinfos[2].rindex('/')
                branch=str(urlinfos[2])[startindex+1:]
                result.append(branch)
        return result
            
        
        
        
    
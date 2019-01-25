package com.xracoon.teamcat.agent.taskrun;

import java.io.IOException;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import org.apache.tools.ant.BuildException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.file.AntZipUtil;
import com.xracoon.teamcat.driver.AgentNotifier;
import com.xracoon.teamcat.driver.ArchiveManager;
import com.xracoon.teamcat.driver.CaseAssign;
import com.xracoon.teamcat.driver.DatasEnum;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.TaskInfo;

public class AgentNotifierImpl  implements AgentNotifier {
	private Logger logger=LoggerFactory.getLogger(AgentNotifierImpl.class);
	private TaskInfo taskInfo;
	private ArchiveManager archiveManager;
	private String archiveRoot;
	private Map<Integer,CaseAssign> caseList;
	private int totalCaseNum;
	private int passedCaseNum;
	private boolean isUpdateResult=false;
	
	public AgentNotifierImpl(){}
	public AgentNotifierImpl(TaskInfo taskInfo,  ArchiveManager archiveManager, boolean isUpdateResult){
		this.taskInfo=taskInfo;
		this.archiveManager=archiveManager;
		this.isUpdateResult=isUpdateResult;
	}
	
	public void setLogger(Logger logger){
		this.logger=logger;
	}
	
	public void resetCaseAssignList(Map<Integer, CaseAssign> caseList){
		this.caseList=new HashMap<Integer,CaseAssign>();
		this.caseList.putAll(caseList);
		totalCaseNum=this.caseList.size();
		passedCaseNum=0;
	}
	

	public Map<Integer,CaseAssign> getNotPassedCases(){
		return Collections.unmodifiableMap(caseList);
	}
	
	public void printResultSummary(){
		if(caseList==null)
			return;
		
		logger.info("-----------------------------------------------");
		logger.info("\t driver execute result summay");
		logger.info("-----------------------------------------------");
		logger.info("total cases: "+totalCaseNum);
		logger.info("passed : "+(totalCaseNum-caseList.size())+" ("+passedCaseNum+")");
		logger.info("still unpassed: "+caseList.size());
		logger.info("-----------------------------------------------");
	}
	
	@Override
	public boolean reportCaseStatus(Long caseId,String caseName, Date start, Date end, int result, String error, String trace) {
//		(int acrtestCaseId, String acrtestCaseName, int acrtaskId, String acrrunUuid, 
//				int acragentId,  Date acrstartTime, Date acrendTime,  int acrresult, int acrbugId,  int acrfailCategoryId,
//				String acrerror, String acrstackTrace, String acrcaseVersion)
		
		if(result==DatasEnum.AutoCaseStatus_Error.getValue())
			result=DatasEnum.AutoCaseStatus_Fail.getValue();
		
		int caseResultId=0;
		try
		{
//			CaseAssign ca=caseList.remove(caseId);
//			if(result==DatasEnum.AutoCaseStatus_Pass.getValue())
//				passedCaseNum++;
//			
//			int caseResultId=service.addCase(caseId/*caseId*/, caseName/*caseName*/, taskInfo.taskID /*taskID*/,   taskInfo.runUUID /*runUUID*/, 
//									taskInfo.agentID/*agent id*/ ,start, end, result, 0/*bugId*/ , 0/*failCategoryId*/,
//									error, trace, null, ca.getRerunId() , isUpdateResult, taskInfo.deviceId);
//			if(caseResultId==-2)
//				logger.info("skip  update  because  rerun still  not passed: "+" case: "+caseId+",   "+caseName+",  result: "+result +(ca.getRerunId()>0?",   rerun="+ca.getRerunId():""));
//			else
//				logger.info((caseResultId==ca.getRerunId()?"update":"insert")+" case: "+caseId+",   "+caseName+",  result: "+result +(ca.getRerunId()>0?",   rerun="+ca.getRerunId():"")+" >>"+caseResultId);
//			
//			if(caseResultId<=0 || result!=DatasEnum.AutoCaseStatus_Pass.getValue())
//			{
//				int runId=ca.getRerunId()<0?caseResultId:ca.getRerunId();
//				caseList.put(caseId, new CaseAssign(caseId, ca.getName(), runId));
//				logger.info("schedule for rerun "+caseId+" on "+runId);
//			}
//				
			return caseResultId>0;
		}
		catch(Exception e)
		{
			logger.error(e.getMessage(),e);
			return false;
		}
	}

	@Override
	public boolean requestArchive(String file,int type) {
		return archiveManager.processArchiveRequest(file, type);
		//archiveManager.processArchiveRequest(null,antStyleFilter,archiveRoot+"/"+taskInfo.taskID+"_"+taskInfo.taskName+"/"+DateUtils.format(new Date(), "yyyyMMddHHmmss"));
	}
	
	public final void archiveLogFile(String logFile){
		archiveManager.processArchiveRequest(logFile, Driver.ARCHIVE_LOG);
	}
	
	public final String getTargetPath(){
		String[] parts=taskInfo.runUUID.split("[$:]");
		String targetPath=archiveRoot+"/"+taskInfo.taskID+"_"+taskInfo.taskConfig.getTaskName()+"/"+parts[0];
		if(parts.length>1)
			targetPath+="/"+parts[1];
		
		return targetPath;
	}
	
	public final void requestArchiveAll(String codePath) throws BuildException, IOException {
		//SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
		//String fileName="archive"+sdf.format(new Date())+".zip";
		
		String fileName=codePath+"/archive_"+taskInfo.runUUID+".zip";
		AntZipUtil.zip(codePath, fileName, null, "**/archive*.zip", logger);
		archiveManager.processArchiveRequest(fileName, Driver.ARCHIVE_ZIPALL);
	}
}

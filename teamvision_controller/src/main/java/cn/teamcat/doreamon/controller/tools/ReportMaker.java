package cn.teamcat.doreamon.controller.tools;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap; 
import java.util.List;
import java.util.Map;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * 创建报告
 * @author Sirui.Zhang
 *
 */
public class ReportMaker {
	
	private HttpClientHelper http =  new HttpClientHelper();

	/**
	 * 获取Email模板
	 * @return
	 * @throws IOException 
	 */
	public static String getEmailTemplate(String path) throws IOException{
		String email = null;
		File file= new File(path);
		FileInputStream fis = new FileInputStream(file);
		InputStreamReader inputStreamReader = new InputStreamReader(fis, "UTF-8");
		BufferedReader in = new BufferedReader(inputStreamReader);
		StringBuffer sBuffer = new StringBuffer();
		String line=null;
		while((line=in.readLine())!=null){
			sBuffer.append(line + "\n");
		}
		fis.close();
		email = sBuffer.toString();
		return email;
	}
	

	/**
	 * 获取邮件基础模块
	 * @param proMapper
	 * @param userMapper
	 * @param historyMapper
	 * @param task
	 * @param projectId
	 * @param taskQId
	 * @param taskName
	 * @return
	 * @throws Exception 
	 */
	public String getCIReport(JSONObject history,Integer projectId,Integer taskQId,String taskName) throws Exception{
		JSONObject projectResponse = http.getProjectDetail(projectId);
		JSONObject projectResult = projectResponse.getJSONObject("result");
		String report = "";
		try {
			report = getEmailTemplate("res/CITaskReport.html");
			report = report.replace("$ProjectName", projectResult.getString("PBTitle"));
			report = report.replace("$Member", history.getString("StartedBy"));
			report = report.replace("$ProjectVersion", history.getString("ProjectVersion"));
			report = report.replace("$BuildVersion", history.getString("BuildVersion"));
			report = report.replace("$TaskName", taskName);
			report = report.replace("$Result", getResult(history.getInt("BuildStatus")));
			if (history.getLong("StartTimeFormat") != 0 && history.getLong("EndTimeFormat") != 0) {
				String start = history.getString("StartTimeFormat");
				String end = history.getString("EndTimeFormat");
				long startTime = Long.valueOf(start.substring(0,start.length() - 2));
				long runtime = (Long.valueOf(end.substring(0,end.length() - 2)) - startTime)/1000;
				report = report.replace("$RunTime", runtime+"s");
				SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
				report = report.replace("$StartTime", sdf.format(startTime));
			}else{
				report = report.replace("$StartTime", "--");
				report = report.replace("$RunTime", "--");
			}
			if (!history.getString("BuildParameterID").equals("null") &&!history.getString("BuildParameterID").equals("")) {
				report = report.replace("$Parameter", http.getParameterGroupName(history.getString("BuildParameterID")));
			}else{
				report = report.replace("$Parameter", "--");
			}
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return report;
	}	
	
	/**
	 * 获取构建详情
	 * @param history
	 * @param report
	 * @return
	 * @throws Exception
	 */
	public String getBuildSummary(JSONObject history,String report) throws Exception{
		report = report.replace("$BuildSummary", getEmailTemplate("res/CITaskBuild.html")).replace("$DeploySummary", "").replace("$Failure", "").replace("$AutoTestingSummary", "");
		report = getCodeInfoBuildLog(history, report);
		if (history.getString("Package").contains(",")) {			
			report = report.replace("$Package", getPackageSummary(history.getString("Package")));
		}else{
			report = replace(report, "$Package", history.getString("Package"));
		}
		return report;
	}
	
	
	
	/**
	 * 获取Package列表详情
	 * @param packageList
	 * @return
	 * @throws IOException 
	 */
	private String getPackageSummary(String pkg) throws IOException{
		String[] packageList = pkg.split(",");
		String template = "";
		if (packageList.length>3) {
			 template = setPackageSummary(packageList);
		}else{
			for (int i = 0; i < packageList.length; i++) {			
				template = template + getEmailTemplate("res/PackageSummary.html");
				packageList[i] = packageList[i].replace("{|}", ",");
				String[] str = packageList[i].split(",");
				template = template.replace("$Package", str[0] + ": " + str[1]);
				if (str[0].contains("apk")||str[0].contains("ipa")) {
					template = template + getEmailTemplate("res/QRCode.html").replace("$CID", i+"");
				}
			}
		}
		return template;
	}

	public List<Map<String,String>>getQRCode(JSONObject history) throws Exception{
		List<Map<String,String>> pathList = new  ArrayList<Map<String,String>>();
		if (history.getString("Package").contains(",")) {			
			String[] packageList = history.getString("Package").split(",");
			if (packageList.length <= 3) {
				for (int i = 0; i < packageList.length; i++) {			
					packageList[i] = packageList[i].replace("{|}", ",");
					String[] str = packageList[i].split(",");
					if (str[0].contains("apk")||str[0].contains("ipa")) {
						Map<String, String> pathMap = new HashMap<String, String>();
						String content = Constants.API.QR_CODE_IMG.replace("$FileID", str[2]).replace("$HistoryID", history.getString("id"));
						String path ="res/" + i + ".jpg";
						QRCodeUtil.encode(content , Constants.LOGO, path, true);
						pathMap.put("cid", i + "");
						pathMap.put("path", path);
						pathList.add(pathMap);
					}
				}
			}
		}
    	return pathList;
	}
	
	private String setPackageSummary(String[] packageList) throws IOException{
		String template = "";
		for (int i = 0; i < packageList.length; i++) {			
			template = template + getEmailTemplate("res/PackageSummary.html");
			packageList[i] = packageList[i].replace("{|}", ",");
			String[] str = packageList[i].split(",");
			template = template.replace("$Package", str[0] + ": " + str[1]);
		}
		return template;
	}
	
	/**
	 * 获取部署详情
	 * @param history
	 * @param task
	 * @param report
	 * @return
	 * @throws Exception
	 */
	public String getDeploySummary(JSONObject history,JSONObject task,String report) throws Exception{
		report = report.replace("$DeploySummary", getEmailTemplate("res/CITaskDeploy.html")).replace("$BuildSummary", "").replace("$Failure", "").replace("$AutoTestingSummary", "");
		JSONObject taskInfoResult = http.getTaskInfo(task.getInt("id"), task.getInt("TaskType"));
		JSONObject service = http.getDeployService(taskInfoResult.getString("deploy_service"));
		report = report.replace("$ServiceName",service.getString("ServiceName"));
		JSONArray serverList = getServerList(taskInfoResult);
		report = report.replace("$ServerSummary",  getServerSummary(serverList));
		report = getCodeInfoBuildLog(history, report);
		return report;
	}
	
	/**
	 * 获取测试详情
	 * @param history
	 * @param task
	 * @param report
	 * @return
	 * @throws Exception
	 */
	public String getTestSummary(JSONObject history,JSONObject task,String report) throws Exception{
		JSONArray taskResultList = http.getTaskResult(history.getInt("id"));
		if (taskResultList.size()>0) {
			report = report.replace("$AutoTestingSummary", getEmailTemplate("res/AutoTestingSummary.html")).replace("$BuildSummary", "").replace("$DeploySummary", "").replace("$Failure", "");
			JSONObject taskResult = taskResultList.getJSONObject(0);
			report = report.replace("$Total", taskResult.getString("Total"));
			report = report.replace("$Passed", taskResult.getString("Pass"));
			report = report.replace("$Failed", taskResult.getString("Fail"));
			report = report.replace("$Aborted", taskResult.getString("Aborted"));
			int taskResultID = taskResult.getInt("id");
			report = report.replace("$HistoryURL", Constants.API.TEST_HISTORY.replace("$CITaskID", history.getString("CITaskID")));
			
			JSONArray caseFailResultList = http.getCaseResult(taskResultID, DatasEnum.AutoCaseStatus_Fail.getValue());
			//目前仅展示失败用例
//			JSONArray caseNotRunResultList = http.getCaseResult(taskResultID, DatasEnum.AutoCaseStatus_NotRun.getValue());
//			JSONArray caseIgnoreResultList = http.getCaseResult(taskResultID, DatasEnum.AutoCaseStatus_Ignore.getValue());
//			if (caseFailResultList.size() + caseNotRunResultList.size() + caseIgnoreResultList.size()>0) {
			if (caseFailResultList.size() > 0) {
				String caseException = "" ;
				report = report.replace("$CaseFailedDetail", getEmailTemplate("res/CaseFailedDetail.html"));
				caseException = getCaseException(caseFailResultList, caseException);
//				caseException = getCaseException(caseNotRunResultList, caseException);
//				caseException = getCaseException(caseIgnoreResultList, caseException);
				report =report.replace("$CaseException", caseException);
			}else{
				report = report.replace("$CaseFailedDetail", "");
			}
		}else{
			report = report.replace("$AutoTestingSummary", "").replace("$BuildSummary", "").replace("$DeploySummary", "").replace("$Failure", "");
		}
		return report;
	}
	
	private String getCaseException(JSONArray caseResultList,String caseException) throws IOException{
		if (caseResultList.size()>0) {
			for (int i = 0; i < caseResultList.size(); i++) {
				JSONObject caseResult = caseResultList.getJSONObject(i);
				caseException = caseException +  getEmailTemplate("res/CaseException.html")
						.replace("$CaseName",caseResult.getString("TestCaseName"))
						.replace("$Result",getCaseResult(Integer.valueOf(caseResult.getString("Result"))))
						.replace("$ErrorMessage",caseResult.getString("Error"))
						.replace("$StackTrace",caseResult.getString("StackTrace"));
			}
		}
		return caseException;
	}
	
	private String getCaseResult(Integer caseResult){
		String result = "";
		switch (caseResult) {
		case 0:
			result = "NotRun";
			break;
		case 1:
			result = "Ignore";
			break;
		case 2:
			result = "Fail";
			break;
		}
		return result;
	}
	
	private JSONArray getServerList(JSONObject taskInfoResult) throws Exception{
		JSONArray serverList = null;
		TaskConfig taskConfig = TaskConfig.fromJson(taskInfoResult.getJSONObject("task_config"));
		String serverIdList = "";
		for (TaskStep taskStep : taskConfig.getAllSteps()) {
			if (taskStep.getType() == 9) {//plagins id待定
				serverIdList = serverIdList + taskStep.getParam("deploy_server") + ",";
			}			
		}
		if (serverIdList.length()>0) {
			 serverList = http.getDeployServer(serverIdList.substring(0,serverIdList.length()-1));
		}
		return serverList;
	}
	
	/**
	 * 获取server列表详情
	 * @param serverList
	 * @return
	 * @throws IOException 
	 */
	private String getServerSummary(JSONArray serverList) throws IOException{
		String serverName = "";
		if (serverList != null && serverList.size()>0) {
			for (int i = 0; i < serverList.size(); i++) {			
				serverName = serverName + getEmailTemplate("res/ServerSummary.html");
				serverName = serverName.replace("$ServerName", serverList.getJSONObject(i).getString("ServerName"));
				serverName = serverName.replace("$Host", serverList.getJSONObject(i).getString("Host"));
			}
		}
		return serverName;
	}
	
	/**
	 * 获取失败详情
	 * @param history
	 * @param report
	 * @return
	 * @throws Exception
	 */
	public String getCIFailureSummary(JSONObject history,String report){
		try {
			report = report.replace("$Failure", getEmailTemplate("res/CITaskFailure.html")).replace("$BuildSummary", "").replace("$DeploySummary", "").replace("$AutoTestingSummary", "");
			report = getCodeInfoBuildLog(history, report);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return report;
	}
	
	/**
	 * 
	 * @param history
	 * @param report
	 * @return
	 * @throws IOException 
	 */
	private String getCodeInfoBuildLog(JSONObject history,String report){
		if (history.getString("BuildLog").contains("{|}")) {
			String buildLog = history.getString("BuildLog").replace("{|}", ",");
			String log[] = buildLog.split(",");
			report = report.replace("$BuildLog",  log[1]);
		}else{
			report = report.replace("$BuildLog",  "");
		}
		try {
			String codeInfo = "";
			if (!history.getString("CodeVersion").equals("null")) {
				if (JSONArray.fromObject(history.getString("CodeVersion")).size() > 0) {
					Map<String,JSONArray> changeLogMap = getChangeLogMap(history);
					JSONArray codeVersionList = JSONArray.fromObject(history.getString("CodeVersion"));
					codeInfo = getEmailTemplate("res/CodeInfoSummary.html");
					String codeSummary = setCodeInfoSummary(codeVersionList, changeLogMap);
					codeInfo = codeInfo.replace("$CodeSummary", codeSummary);
				} 
			}
			report = report.replace("$CodeInfo",codeInfo);
		} catch (Exception e) {
			report = report.replace("$CodeInfo","");
		}
		return report;
	}
	
	private String setCodeInfoSummary(JSONArray codeVersionList,Map<String,JSONArray> changeLogMap) throws IOException{
		String codeSummary = "";
		for (int i = 0; i < codeVersionList.size(); i++) {
			JSONObject codeVersion = codeVersionList.getJSONObject(i);
			String codeUrl = codeVersion.getString("repo");
			codeSummary = codeSummary + getEmailTemplate("res/CodeUrlSummary.html").replace("$CodeUrl", codeUrl);
			if (changeLogMap.get(codeUrl) != null) {
				JSONArray changelogList = changeLogMap.get(codeUrl);
				String changeLogSummary ="";
				for (int j = 0; j < changelogList.size(); j++) {
					JSONObject changeLog = changelogList.getJSONObject(j);
					changeLogSummary = changeLogSummary+ getEmailTemplate("res/ChangeLogSummary.html");
					changeLogSummary = changeLogSummary.replace("$Number", j+1+"");
					changeLogSummary = changeLogSummary.replace("$Version", changeLog.getString("version"));
					changeLogSummary = changeLogSummary.replace("$Timestamp", changeLog.getString("timestamp"));
					changeLogSummary = changeLogSummary.replace("$Message", changeLog.getString("message").replace("\r\n", "<br>"));
					changeLogSummary = changeLogSummary.replace("$Author", changeLog.getString("author"));
				}
				codeSummary = codeSummary + changeLogSummary;
			}else if (codeVersion.containsKey("version")) {
				codeSummary = codeSummary + getEmailTemplate("res/CodeVersionSummary.html");
				codeSummary = codeSummary.replace("$Version", codeVersion.getString("version"));
			}
		}
		return codeSummary;
	}
	
	/**
	 * 获取ChangeLog
	 * @param history
	 * @return
	 * @throws Exception 
	 */
	public Map<String,JSONArray> getChangeLogMap(JSONObject history) throws Exception{
		Map<String,JSONArray> changeLogMap =  new HashMap<String, JSONArray>();
		String change = http.getChangeLog(history.getInt("id"));
		if (!change.equals("")) {
			if (JSONArray.fromObject(JSONObject.fromObject(change).getString("change_log")).size() > 0) {
				JSONArray changeLogList =JSONArray.fromObject(JSONObject.fromObject(change).getString("change_log"));
				for (int i = 0; i < changeLogList.size(); i++) {
					JSONObject changeLog = changeLogList.getJSONObject(i);
					changeLogMap.put(changeLog.getString("repo"), changeLog.getJSONArray("changes"));
				}
			}
		}
		return changeLogMap;
	}
	
	
	private String replace(String report,String oldChar ,String newChar){
		if (!newChar.equals("null")) {
			report = report.replace(oldChar, newChar);
		}else{
			report = report.replace(oldChar,  "");
		}
		return report;
	}
	
	
	private String getResult(Integer buildStatus){
		String result = "";
		switch (buildStatus) {
		case 1:
			result = "Completed";
			break;
		case 2:
			result = "Fail";
			break;
		case 3:
			result = "Aborted";
			break;
		}
		return result;
	}

}
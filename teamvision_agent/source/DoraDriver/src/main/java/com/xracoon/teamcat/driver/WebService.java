package com.xracoon.teamcat.driver;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import com.xracoon.teamcat.models.ci.CiAutoCaseInfo;
import com.xracoon.teamcat.models.ci.CiTaskBasic;
import com.xracoon.teamcat.utils.GsonHelper;
import com.xracoon.teamcat.utils.PropertiesTools;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.driver.step.DeployServerInfo;
import com.xracoon.teamcat.driver.step.DeployFileStep.DeployFileItem;
import com.xracoon.teamcat.plugin.DeployInfo;
import com.xracoon.teamcat.plugin.TaskConfig;
import com.xracoon.teamcat.utils.HttpUtils;
import com.xracoon.teamcat.utils.scm.Revision;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.util.basekit.ArraysEx;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.security.Crypto;
import com.xracoon.util.basekit.security.auth.Credential;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class WebService {
	public static int OK=1;
	private static Logger logger=LoggerFactory.getLogger(WebService.class);
	public static String baseUrl=null;
	private static final String channel = "CI_AGENT_"+PropertiesTools.getProperty("agent.key");
	static{
		String basePath= PropertiesTools.basePath;
		InputStream is=null;
		try{
			//String configFile= ConsoleLauncher.basePath;
			if(StringEx.isBlank(basePath))
				throw new Exception("config file agent.properties not found");
				
			File file=new File(basePath, "agent.properties");
			is= FilesEx.openInputStream(file.getAbsolutePath());
			Properties prop = new Properties();
			prop.load(is);
			if(prop.containsKey("server.host")){
				baseUrl=prop.getProperty("server.host").trim();
				logger.info("server.host : "+baseUrl);
			}
			else
				throw new Exception("'server.host' not found in "+basePath);
			
			is.close();
		}catch(Exception e){
			logger.error("agent.properties load failed");
			e.printStackTrace();
			if(is!=null)
				try {
					is.close();
				} catch (IOException e1) {
					e1.printStackTrace();
				}
		}
	}
	public static String baseUrlCI=baseUrl+"/api/ci";
	public static String baseUrlCommon=baseUrl+"/api/common";
	public static String taskInfo=baseUrlCI+"/task/get_task";
	public static String deployInfo= baseUrlCI+"/deploy_service";
	public static String credential=  baseUrlCI+"/crendential";
	public static String lastVersion= baseUrlCI+"/task/${task_id}/task_histories";
	public static String updateScmData= baseUrlCI+"/task_history";
	public static String tqUpload=baseUrlCI+"/task/upload_package";
	public static String deployReplaceFile = baseUrlCI+"/deploy_service_replace_config";
	public static String deployServerInfo= baseUrlCI+"/deploy_server";
	public static String URL_GetParameterGroup= baseUrlCI+"/task/parameter_group";
	public static String URL_ServiceHost=baseUrlCI+"/service_hosts"; 
	public static String URL_TestCases=baseUrlCI+"/auto_cases";
	public static String URL_UpdateCaseResult= baseUrlCI+"/auto_case_result";
	public static String URL_QueryCaseResults= baseUrlCI+"/auto_case_results";
	public static String URL_QueryTaskQueueInfo= baseUrlCommon+"/task_queue";
	public static String URL_QueryTaskBasic = baseUrlCI+"/task_basic";
	public static String URL_QueryAutoCases = baseUrlCI+"/auto_cases";
	public static String URL_Simple_MQ = baseUrlCommon+"/simple_mq";
	
	public static void queryTaskConfig(TaskInfo info) throws Exception{
		Map<String,String> params=new HashMap<>();
		params.put("task_id", info.taskID+"");
		params.put("task_type", info.taskType+"");
		
		HttpEntity entity=HttpUtils.httpRequest(taskInfo, "GET", params, null, false).getEntity();
		String respText=EntityUtils.toString(entity, "UTF-8");
		if(File.pathSeparator.equals(":"))
			respText.replace("\r", "");
		JSONObject json=JSONObject.fromObject(respText);
		JSONObject result=json.getJSONObject("result");
		
		//info.runUUID=result.getString("runUUID");
		info.taskConfig=TaskConfig.fromJson(result.getJSONObject("task_config"));
		info.taskConfig.setTaskId(info.taskID);
		info.taskConfig.setTaskType(info.taskType);
		info.taskConfig.setTaskName(info.taskConfig.getSection("basic_section").getSteps().get(0).getParam("TaskName"));
		info.taskConfig.setTaskQueueId(info.taskQueueID);
		
		info.taskConfig.setDeployConfigId(result.containsKey("deploy_service")?result.getInt("deploy_service"):null);
		if(info.taskConfig.getDeployConfigId()!=null && info.taskConfig.getDeployConfigId() > 0){
			info.taskConfig.setDeployInfo(WebService.deployInfo(info.taskConfig.getDeployConfigId()));
		}
	}
	
	public static Map<String,Object> queryTaskQueueInfo(long id) throws Exception{
		Map<String,Object> map=new LinkedHashMap<>();
		HttpEntity entity=HttpUtils.httpRequest(URL_QueryTaskQueueInfo+"/"+id, "GET", null, null, false).getEntity();
		JSONObject json=JSONObject.fromObject(EntityUtils.toString(entity, "UTF-8"));
		JSONObject result=json.getJSONObject("result");
		for(Object k:result.keySet().toArray(new Object[0]))
			map.put(k.toString(), result.get(k.toString()));
		return map;
	}

	public static void sendErrorMsg(String message) throws Exception{
		Map<String,String> params=new HashMap<>();
		params.put("channel", channel);
		params.put("message", message);
		HttpEntity entity=HttpUtils.httpRequest(URL_Simple_MQ, "POST", params, null, true).getEntity();
		String content=EntityUtils.toString(entity, "UTF-8");
		JSONObject json=JSONObject.fromObject(content);
		if(json.getInt("code")==201){
			logger.info("Send ErrMessage Success");
		}else{
			logger.error("Send ErrMessage Failed");
		}
	}

	public static CiTaskBasic queryTaskBasic(Integer taskId) throws Exception{
		HttpEntity entity=HttpUtils.httpRequest(URL_QueryTaskBasic+"/"+taskId, "GET", null, null, false).getEntity();
		String result=EntityUtils.toString(entity, "UTF-8");
		CiTaskBasic ciTaskBasic= GsonHelper.getGson().fromJson(result,CiTaskBasic.class);
		return ciTaskBasic;
	}

	public static CiAutoCaseInfo queryAutoCases(Map<String,String> params) throws Exception{
		HttpResponse response=HttpUtils.httpRequest(URL_QueryAutoCases, "GET", params, null, false);
		if(response.getStatusLine().getStatusCode()!=200){
			logger.error("Query Case failed status code is :"+response.getStatusLine().getStatusCode());
			throw new RuntimeException("Query case failed");
		}else{
			HttpEntity entity=response.getEntity();
			String result=EntityUtils.toString(entity, "UTF-8");
			CiAutoCaseInfo ciAutoCaseInfo =GsonHelper.getGson().fromJson(result,CiAutoCaseInfo.class);
			return ciAutoCaseInfo;
		}
	}
		
	public static DeployInfo deployInfo(int deployId) throws Exception{
		HttpEntity entity=HttpUtils.httpRequest(deployInfo+"/"+deployId, "GET", null, null, false).getEntity();
		JSONObject json=JSONObject.fromObject(EntityUtils.toString(entity, "UTF-8"));
		JSONObject result=json.getJSONObject("result");
		return DeployInfo.fromJson(result);
	}
	
	public static Credential queryCredential(long id) throws Exception{
		HttpEntity entity=HttpUtils.httpRequest(credential+"/"+id, "GET", null, null, false).getEntity();
		String content=EntityUtils.toString(entity, "UTF-8");
		JSONObject json=JSONObject.fromObject(content);
		JSONObject result=json.getJSONObject("result");
		String user=result.getString("UserName");
		
		byte[] key="Hsbjiademlsdftu9".getBytes();
		char[] passwd=new String(Crypto.decrytSymm(StringEx.hex2Bytes(result.getString("Password")), "AES/CBC/NoPadding", key, key)).toCharArray();
		int credType=result.getInt("CredentialType");
		String sshKey=result.getString("SSHKey");
//		if(!StringEx.isBlank(sshKey) && sshKey.contains("---"))
//			sshKey=Crypto.trimDesc(Arrays.asList(sshKey.split("[\\r\\n]+")));
		logger.info("SecretKeyPem user : "+user+" sshKey: "+sshKey+" passwd: "+passwd.toString());
		if(credType==1)
			return Credential.Plain(user, passwd);
		else{
			return Credential.SecretKeyPem(user, sshKey, passwd);
		}
	}
	public static String getCurrentBuildId(long taskId) throws Exception{
		logger.info(String.valueOf(taskId));
		CloseableHttpResponse response = HttpUtils.httpRequest(StringEx.resolveToken(lastVersion, ArraysEx.toMap("task_id",taskId+"")), "GET", null, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		JSONObject json=JSONObject.fromObject(rspText);
		String currentbuildId=json.getJSONObject("result").getJSONObject("all_histories")
				.getJSONArray("results").getJSONObject(0).getString("BuildVersion");
		return currentbuildId;
	}
	public static Map<String,String> getLastVersion(long taskId) throws Exception{
		Map<String,String> versionMap=new HashMap<>();	
		//非必填自动的问题
		CloseableHttpResponse response = HttpUtils.httpRequest(StringEx.resolveToken(lastVersion, ArraysEx.toMap("task_id",taskId+"")), "GET", null, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		JSONObject json=JSONObject.fromObject(rspText);
		String lastCodeVer=json.getJSONObject("result").getString("latest_code_version");
		if(!StringEx.isBlank(lastCodeVer) && !lastCodeVer.equalsIgnoreCase("null")){
			JSONArray map= JSONArray.fromObject(json.getJSONObject("result").getString("latest_code_version"));
			for(int i=0; i<map.size(); i++){
				String repo=map.getJSONObject(i).getString("repo");
				int idx=repo.toLowerCase().indexOf(".git/");
				if(idx>0)
					repo=repo.substring(0, idx+4);
				versionMap.put(repo, map.getJSONObject(i).getString("version"));
			}
		}
		return versionMap;
	}
	
	public static Map<String,String> getParameters(String paramId) throws Exception{
		Map<String,String> tokenMap=new HashMap<>();
		if(StringEx.isBlank(paramId))
			return tokenMap;
		
		//非必填自动的问题
		CloseableHttpResponse response = HttpUtils.httpRequest(URL_GetParameterGroup+"/"+paramId, "GET", null, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		JSONObject json=JSONObject.fromObject(rspText).getJSONObject("result");
		if(json.getBoolean("is_active")){
			tokenMap.put(Driver.TOK_PARAMGROUP, json.getString("group_name"));
			if(json.getBoolean("enable_plugin_settings"))
			{
			  tokenMap.put("step_plugin_is_enable", json.getJSONArray("step_plugin_is_enable").toString());	
			}
			if(!json.get("parameters").equals(null))
			{
				JSONArray map= json.getJSONArray("parameters");
				for(int i=0; i<map.size(); i++)
					tokenMap.put(map.getJSONObject(i).getString("key"), map.getJSONObject(i).getString("value"));
			}
		}
		return tokenMap;
	}
	
	public static boolean updateHistoryData(long historyId, Map<String,String> versionMap,
				Map<String,List<Revision>> changeSetMap, String packageInfo) throws Exception{
		Map<String, String> params=new HashMap<>();
		if(versionMap!=null && !versionMap.isEmpty()){
			JSONArray codeVersions=new JSONArray();
			for(String k:versionMap.keySet()){
				JSONObject obj=new JSONObject();
				obj.put("repo", k);
				obj.put("version", versionMap.get(k));
				codeVersions.add(obj);
			}
			params.put("CodeVersion", codeVersions.toString());
		}
		if(changeSetMap!=null && !changeSetMap.isEmpty()){
			JSONArray changes=new JSONArray();
			for(String k:changeSetMap.keySet()){
				JSONObject obj=new JSONObject();
				obj.put("repo", k);
				obj.put("changes", JSONArray.fromObject(changeSetMap.get(k)));
				changes.add(obj);
			}
			params.put("ChangeLog", changes.toString());
		}
		if(!StringEx.isBlank(packageInfo))
			params.put("PackageInfo", packageInfo);
		
		CloseableHttpResponse response = HttpUtils.httpRequest(updateScmData+"/"+historyId+"/", "PATCH", params, null, false);
		int statusCode = response.getStatusLine().getStatusCode();
		return statusCode==200;
	}
	
	public static boolean tqUpload(long tqId, String file, int type) throws Exception{
		Map<String,String> params=new HashMap<>();
		params.put("tq_id", tqId+"");
		params.put("file_type", type+"");
		params.put("upload_file", file);
		
		HttpEntity entity=HttpUtils.httpRequest(tqUpload, "POST", params, null, true).getEntity();
		String content=EntityUtils.toString(entity, "UTF-8");
		JSONObject json=JSONObject.fromObject(content);
		logger.info(file+" --> "+content);
		return json.getInt("result")>0;
	}
	
	public static Map<Long, DeployFileItem> queryDeployReplaceFile(long deployId) throws Exception{
		Map<Long, DeployFileItem> deployfileMap=new HashMap<>();
		CloseableHttpResponse response = HttpUtils.httpRequest(deployReplaceFile+"/"+deployId, "GET", null, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		JSONObject json=JSONObject.fromObject(rspText);
		JSONArray array=null;
		if((array=json.getJSONArray("result"))!=null && array.size()>0){
			if((array=array.getJSONObject(0).getJSONArray("replace_target_map"))!=null && array.size()>0){
				JSONArray map= array;
				for(int i=0; i<map.size(); i++){
					JSONObject obj=map.getJSONObject(i);
					deployfileMap.put(obj.getLong("file_id"), 
							new DeployFileItem(obj.getLong("file_id"), obj.getString("file_url"), obj.getString("file_name"), obj.getString("replace_targets")));
				}
			}
		}
		return deployfileMap;
	}
	
	public static DeployServerInfo queryDeployServer(long serverId) throws Exception{
		CloseableHttpResponse response = HttpUtils.httpRequest(deployServerInfo+"/"+serverId, "GET", null, null, false);
		JSONObject json=JSONObject.fromObject(EntityUtils.toString(response.getEntity(), "UTF-8")).getJSONObject("result");
		DeployServerInfo serverInfo=new DeployServerInfo();
		serverInfo.setId(json.getLong("id"));
		serverInfo.setServerName(json.getString("ServerName"));
		serverInfo.setHost(json.getString("Host"));
		serverInfo.setRemoteDir(json.getString("RemoteDir"));
		serverInfo.setPort(json.getInt("Port"));
		serverInfo.setCredentialId(json.getLong("Credential"));
		return serverInfo;
	}


	public static Map<String, String> queryHosts(int envId) throws Exception{
		Map<String,String> hosts=new HashMap<>();	
		CloseableHttpResponse response = HttpUtils.httpRequest(URL_ServiceHost+"?page_size="+Integer.MAX_VALUE+"&EnvID="+envId, "GET", null, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		JSONObject json=JSONObject.fromObject(rspText);
		JSONArray hostList=json.getJSONObject("result").getJSONArray("results");
		for(int i=0,len=hostList.size(); i<len; i++){
			JSONObject jhost=hostList.getJSONObject(i);
			String ip=jhost.getString("HostIP");
			String hostNames=jhost.getString("HostService");
			hosts.put(hostNames,ip);
		}
		return hosts;
	}
	public static List<TestCase> queryCases(String caseList) throws Exception{
		List<TestCase> caseLists=new ArrayList<>();
		CloseableHttpResponse response = HttpUtils.httpRequest(URL_TestCases+"?page_size="+Integer.MAX_VALUE+"&id__in="+caseList, "GET", null, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		JSONObject json=JSONObject.fromObject(rspText);
		JSONArray jcaseList=json.getJSONObject("result").getJSONArray("results");
		for(int i=0,len=jcaseList.size(); i<len; i++){
			JSONObject jcase=jcaseList.getJSONObject(i);
			TestCase acase=new TestCase(jcase.getLong("id"), jcase.getString("PackageName"), 
					jcase.getString("ClassName"), jcase.getString("CaseName"));			
			caseLists.add(acase);
		}
		return caseLists;
	}
	
	public static class CaseMapItem{
		public long caseId;
		public long resultId;
		public String caseName;
	}
	public static Map<String, CaseMapItem> queryCaseResultsIdMap(Long TaskResultID) throws Exception{
		Map<String, CaseMapItem> caseIdToIDMap =new HashMap<>();
		CloseableHttpResponse response = HttpUtils.httpRequest(URL_QueryCaseResults+"?page_size="+Integer.MAX_VALUE+"&TaskResultID="+TaskResultID, "GET", null, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		JSONObject json=JSONObject.fromObject(rspText);
		JSONArray jcaseResultList=json.getJSONObject("result").getJSONArray("results");
		for(int i=0,len=jcaseResultList.size(); i<len; i++){
			JSONObject jcase=jcaseResultList.getJSONObject(i);
			CaseMapItem info=new CaseMapItem();
			info.caseName=jcase.getString("TestCaseName");
			info.caseId=jcase.getLong("TestCaseID");
			info.resultId=jcase.getLong("id");
			caseIdToIDMap.put(info.caseName, info);
		}
		return caseIdToIDMap;
	}
	public static void  updateCaseResult(Long taskResultID, Date start, Date end, int result, String error, String trace,Long testCaseId) throws Exception {
		SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'+08:00'");
		Map<String,String> params=new HashMap<>();
		
		params.put("TaskResultID", taskResultID.toString());
		params.put("StartTime", sdf.format(start.getTime()));
		params.put("EndTime", sdf.format(end.getTime()));
		params.put("Result", result+"");
		params.put("TestCaseID", testCaseId.toString());
		if(!StringEx.isBlank(error))
			params.put("Error", error);
		if(!StringEx.isBlank(trace))
			params.put("StackTrace", trace);
		
//		String method=id!=null?"PATCH":"POST";
//		String url=URL_QueryCaseResults+"/";
//		if(id!=null)
//			url+="/"+id+"/";
		CloseableHttpResponse response = HttpUtils.httpRequest(URL_QueryCaseResults, "POST", params, null, false);
		String rspText=EntityUtils.toString(response.getEntity(), "UTF-8");
		logger.warn(testCaseId.toString());
		try{
			JSONObject json=JSONObject.fromObject(rspText);
			if(json.getInt("code")!=201)
			{
				throw new Exception(rspText);
			}
		}catch(Exception e){
			logger.error(e.getLocalizedMessage());
		}
	}
//----------------
	

	
	public static int simpleReqest(String method, String url, Map<String,String> params) throws Exception{		
		HttpEntity entity=HttpUtils.httpRequest(url, method, params, null, false).getEntity();
		JSONObject json=JSONObject.fromObject(EntityUtils.toString(entity, "UTF-8"));
//		if(json.getInt("code")!=OK){
//			logger.error("error respose status: "+json.getString("msg"));
//		}
		return json.getInt("code");
	}
	
}

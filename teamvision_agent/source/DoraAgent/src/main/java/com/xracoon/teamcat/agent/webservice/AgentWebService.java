package com.xracoon.teamcat.agent.webservice;

import static com.xracoon.teamcat.driver.WebService.simpleReqest;

import java.util.HashMap;
import java.util.Map;

import com.xracoon.teamcat.agent.models.ConfigInfo;
import com.xracoon.teamcat.agent.models.DicConfigs;
import com.xracoon.teamcat.utils.GsonHelper;
import org.apache.commons.lang3.StringUtils;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.config.AgentConfig;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.utils.HttpUtils;

import net.sf.json.JSONObject;

public class AgentWebService {
	private static Logger logger=LoggerFactory.getLogger(WebService.class);
	public static String api= WebService.baseUrl+"/api";
	public static String ci= WebService.baseUrlCI;
	public static String common=api+"/common";
	
	public static String agentInfo=common+"/agent";
	public static String agentUpdate=ci+"/agent/update_agent_status";
	
	public static String tqDone=ci+"/task/tq_done";
	public static String addMessage = ci.replace("/api/ci", "/ci/")+"dashboard/add_message";

	public static String getConfigUrl=common+"/dicconfig";

	public static DicConfigs getConfigByConfigType(Integer configType){
		String url = getConfigUrl+"/"+configType+"/dicconfigs";
		HttpEntity entity;
		String content;
		try {
			entity=HttpUtils.httpRequest(url,"GET",null,null,false).getEntity();
			content=EntityUtils.toString(entity,"UTF-8");
		} catch (Exception e) {
			logger.error("get config failed");
			e.printStackTrace();
			return null;
		}
		logger.info("get conf from server: "+content);
		return GsonHelper.getGson().fromJson(content,DicConfigs.class);
	}

	public static Long getAgentTimeOutMileSec(){
		DicConfigs dicConfigs=getConfigByConfigType(26);
		for(ConfigInfo configInfo:dicConfigs.getResult()){
			if(configInfo.getDicDataName().equals("AgentTimeOutMileSec")){
				return configInfo.getDicDataValue().longValue();
			}
		}
		return null;
	}
	public static HashMap<String,String> getRedisConf(){
		DicConfigs dicConfigs=getConfigByConfigType(26);
		HashMap<String,String> map=null;
		if(dicConfigs.getResult().size()>0){
			map=new HashMap<>();
			for(ConfigInfo configInfo:dicConfigs.getResult()){
				if(configInfo.getDicDataName().equals("RedisAddress")){
					map.put("RedisAddress",configInfo.getDicDataDesc());
				}
				if(configInfo.getDicDataName().equals("RedisPort")){
					map.put("RedisPort",configInfo.getDicDataDesc());
				}
				if(map.size()==2){
					break;
				}
			}
		}
		return map;
	}
	
	public static int agentUpate(String agentKey, int status) throws Exception{
		Map<String,String> params=new HashMap<>();
		params.put("agent_id", agentKey);
		params.put("status", status+"");
		return simpleReqest("GET", agentUpdate, params);
	}
	
	public static void agentInfo(AgentConfig aconf) throws Exception{	
		HttpEntity entity=HttpUtils.httpRequest(agentInfo+"/"+aconf.agentKey, "GET", null, null, false).getEntity();
		String content=EntityUtils.toString(entity, "UTF-8");
		JSONObject json=JSONObject.fromObject(content);
		JSONObject result=json.getJSONObject("result");
		logger.info("Agent conf : "+result);
		aconf.agentId=result.getInt("id");
		aconf.agentName=result.getString("Name");
		aconf.agentPort=result.getInt("AgentPort");
		if(StringUtils.isNotBlank(result.getString("AgentWorkSpace")))
			aconf.workDir=result.getString("AgentWorkSpace");
		if(StringUtils.isNotBlank(result.getString("BuildToolsDir")))
			aconf.buillToolsPath=result.getString("BuildToolsDir");
	}
	
	public static int tqDone(long tqId, int status, String errorMsg ) throws Exception{
		Map<String,String> params=new HashMap<>();
		params.put("tq_id", tqId+"");
		params.put("status", status+"");
		params.put("error_msg", errorMsg);
		
		return simpleReqest("GET", tqDone,params);
	}
	
	public static Boolean andMessage(long tqId, String msg) throws Exception{
		Map<String,String> params=new HashMap<>();
		params.put("tq_id", tqId+"");
		params.put("msg", msg+"{ENTER}");
		boolean status = false;		
		CloseableHttpResponse response = HttpUtils.httpRequest(addMessage, "POST", params, null, true);
		int statusCode = response.getStatusLine().getStatusCode();
		if (statusCode == 200) {
			status = true;
		}
		return status;
	}
}

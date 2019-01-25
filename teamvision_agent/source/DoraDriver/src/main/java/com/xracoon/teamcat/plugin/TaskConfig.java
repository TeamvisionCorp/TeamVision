package com.xracoon.teamcat.plugin;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.bouncycastle.jcajce.provider.symmetric.Threefish;

import com.xracoon.teamcat.driver.step.BuildStep.StepType;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class TaskConfig implements Serializable {
	private static final long serialVersionUID = -3633163519132066640L;
	
	public static final String SECTION_PRE="pre_section";
	public static final String SECTION_BASIC="basic_section";
	public static final String SECTION_SCM="scm_section";
	public static final String SECTION_BUILD="build_section";
	public static final String SECTION_POST="post_section";
	
	private Long taskId;
	private String taskName;
	private Long taskType;
	private Long taskQueueId;
	private String tokenGroup;
	private String buildId;
	
	private Map<String, TaskSection> sectionMap;
	private Integer deployConfigId;
	private DeployInfo deployInfo;
	
	public static TaskConfig fromJson(JSONObject json) throws Exception{
		TaskConfig conf=new TaskConfig();
		Map<String, TaskSection> sectionMap=new LinkedHashMap<>();
		sectionMap.put(SECTION_PRE, toSection(json,SECTION_PRE));
		sectionMap.put(SECTION_BASIC, toSection(json,SECTION_BASIC));
		sectionMap.put(SECTION_SCM, toSection(json, SECTION_SCM));
		sectionMap.put(SECTION_BUILD, toSection(json, SECTION_BUILD));
		sectionMap.put(SECTION_POST, toSection(json, SECTION_POST));
		conf.setSectionMap(sectionMap);
		return conf;
	}
	public static TaskSection toSection(JSONObject taskjson, String sectionName) throws Exception{
		JSONObject json=taskjson.getJSONObject(sectionName);
		TaskSection sect=new TaskSection();
		sect.setSectionId(json.getInt("section_id"));
		sect.setSectionName(sectionName);
		List<TaskStep> steps=new ArrayList<>();
		JSONArray jSteps=json.getJSONArray("plugins");
		for(@SuppressWarnings("unchecked")Iterator<JSONObject> iter=jSteps.iterator(); iter.hasNext();){
			JSONObject jStep=iter.next();
			TaskStep step=toStep(jStep);
			step.setSectionName(sectionName);
			step.setSectionId(sect.getSectionId());
			steps.add(step);
		}
		Collections.sort(steps);
		sect.setSteps(steps);
		return sect;
	}
	public static TaskStep toStep(JSONObject jStep) throws Exception{
		TaskStep step=new TaskStep();
		int stepId=jStep.containsKey("plugin_id")?jStep.getInt("plugin_id"):0;
		step.setType(StepType.fromId(stepId));
		step.setOrder(jStep.getInt("order"));
		step.setEnable(jStep.containsKey("is_enable") && jStep.getString("is_enable").equalsIgnoreCase("On"));
		toParamMap(step,jStep.getJSONArray("parameter"));
		
		return step;
	}
	public static void toParamMap(TaskStep step, JSONArray paramsJson){
		Map<String, String> map=new HashMap<>();
		Map<String, List<String>> mapList=new HashMap<>();
		for(int i=0; i<paramsJson.size(); i++ ){
			JSONObject json=paramsJson.getJSONObject(i);
			String key=json.getString("name").trim();
			//maplist里有, 直接放maplist
			if(mapList.containsKey(key))
				mapList.get(key).add(json.getString("value").trim());
			//maplist里没有，map里有, 从map移到maplist,新值直接放到maplist
			else if(map.containsKey(key)){
				List<String> list=new ArrayList<>();
				mapList.put(key, list);
				list.add(map.remove(key));
				list.add(json.getString("value").trim());
			}
			//maplist里没有，map里也没有，放到map
			else
				map.put(key, json.getString("value").trim());
		}
		step.setParams(map);
		step.setParamsMultiValue(mapList);
	} 
	
	public Map<String, TaskSection> getSectionMap() {
		return sectionMap;
	}
	public void setSectionMap(Map<String, TaskSection> setcionMap) {
		this.sectionMap = setcionMap;
	}
	public TaskSection getSection(String sectionName){
		return sectionMap!=null?sectionMap.get(sectionName):null;
	}
	public List<TaskStep> getAllSteps(){
		List<TaskSection> allSections=new ArrayList<>(sectionMap.values());
		Collections.sort(allSections);
		
		List<TaskStep> allSteps=new ArrayList<>();
		for(TaskSection ts : allSections){
			//section中的steps解析时已排好序
			allSteps.addAll(ts.getSteps());
		}
		return allSteps;
	}
	public boolean isDeployService(){
		return deployInfo!=null;
	}
	
	public DeployInfo getDeployInfo() {
		return deployInfo;
	}
	public void setDeployInfo(DeployInfo deployInfo) {
		this.deployInfo = deployInfo;
	}
	public Long getTaskId() {
		return taskId;
	}
	public void setTaskId(Long taskId) {
		this.taskId = taskId;
	}
	public String getTaskName() {
		return taskName;
	}
	public void setTaskName(String taskName) {
		this.taskName = taskName;
	}
	public long getTaskType() {
		return taskType;
	}
	public void setTaskType(long taskType) {
		this.taskType = taskType;
	}
	public Long getTaskQueueId() {
		return taskQueueId;
	}
	public void setTaskQueueId(Long taskQueueId) {
		this.taskQueueId = taskQueueId;
	}
	public Integer getDeployConfigId() {
		return deployConfigId;
	}
	public void setDeployConfigId(Integer deployConfigId) {
		this.deployConfigId = deployConfigId;
	}
	public String getTokenGroup() {
		return tokenGroup;
	}
	public void setTokenGroup(String tokenGroup) {
		this.tokenGroup = tokenGroup;
	}
	public String getBuildId() {
		return buildId;
	}
	public void setBuildId(String buildId) {
		this.buildId = buildId;
	}
}

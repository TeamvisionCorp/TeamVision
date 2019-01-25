package cn.teamcat.doreamon.controller.tools;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class TaskConfig {
	private Map<String, TaskSection> sectionMap;
	public static TaskConfig fromJson(JSONObject json){
		TaskConfig conf=new TaskConfig();
		Map<String, TaskSection> sectionMap=new LinkedHashMap<>();
		sectionMap.put("pre_section", toSection(json.getJSONObject("pre_section")));
		sectionMap.put("basic_section", toSection(json.getJSONObject("basic_section")));
		sectionMap.put("scm_section", toSection(json.getJSONObject("scm_section")));
		sectionMap.put("build_section", toSection(json.getJSONObject("build_section")));
		sectionMap.put("post_section", toSection(json.getJSONObject("post_section")));
		conf.setSectionMap(sectionMap);
		return conf;
	}
	public static TaskSection toSection(JSONObject json){
		TaskSection sect=new TaskSection();
		sect.setSectionId(json.getInt("section_id"));
		List<TaskStep> steps=new ArrayList<>();
		JSONArray jSteps=json.getJSONArray("plugins");
		for(@SuppressWarnings("unchecked")Iterator<JSONObject> iter=jSteps.iterator(); iter.hasNext();){
			JSONObject jStep=iter.next();
			steps.add(toStep(jStep));
		}
		Collections.sort(steps);
		sect.setSteps(steps);
		return sect;
	}
	public static TaskStep toStep(JSONObject jStep){
		TaskStep step=new TaskStep();
		step.setType(jStep.containsKey("plugin_id")?jStep.getInt("plugin_id"):0);
		step.setOrder(jStep.getInt("order"));
		step.setEnable(jStep.containsKey("is_enable") && jStep.getString("is_enable").equalsIgnoreCase("On"));
		step.setParams(toParamMap(jStep.getJSONArray("parameter")));
		return step;
	}
	public static Map<String,String> toParamMap(JSONArray paramsJson){
		Map<String, String> map=new HashMap<>();
		for(int i=0; i<paramsJson.size(); i++ ){
			JSONObject json=paramsJson.getJSONObject(i);
			map.put(json.getString("name"), json.getString("value"));
		}
		return map;
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
}

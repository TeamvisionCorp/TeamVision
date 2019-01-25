package com.xracoon.teamcat.plugin;

import java.awt.print.Printable;
import java.io.Serializable;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.tmatesoft.sqljet.core.internal.lang.SqlParser.indexed_column_return;

import com.xracoon.teamcat.driver.step.BuildStep.StepType;
import com.xracoon.util.basekit.StringEx;

public class TaskStep implements Comparable<TaskStep>, Serializable {	
	private static final long serialVersionUID = -491241930015379968L;
	private static Logger logger=LoggerFactory.getLogger(TaskStep.class);
	
	private StepType type;
	private int order;
	private String sectionName;
	private int sectionId;
	private boolean isEnable;
	private Map<String, String> params;
	private Map<String, List<String>> paramMultiValue;
	
	public void resolveTokens(Map<String, String> tokens){
		this.setStepEnableByParameter(tokens.get("step_plugin_is_enable"));
		for(String k: params.keySet())
		{
			params.put(k, StringEx.resolveToken(params.get(k),tokens));
		}
		for(String k: paramMultiValue.keySet()){
			List<String> list=paramMultiValue.get(k);
			for(int i=0; i<list.size(); i++)
				list.set(i, StringEx.resolveToken(list.get(i), tokens));
		}
	}
	
    private void setStepEnableByParameter(String plugin_is_enable)
    {
    	    String pluginKey=String.valueOf(this.sectionId)+"_"+String.valueOf(this.type.getId())+"_"+String.valueOf(this.order);
    	    if(plugin_is_enable==null)
    	    {
    	    	  return;
    	    }
    	    String[] enableList=plugin_is_enable.replace("[","").replace("]","").split(",");
    	    for(String enableValue:enableList)
    	    {
    	    	    if(enableValue.startsWith("\""+pluginKey))
    	    	    {
    	    	    	   String enableStatus=enableValue.replaceAll("\"","").replace(pluginKey+":","");
    	    	    	   if(enableStatus.equals("On"))
    	    	    	   {
    	    	    		   this.setEnable(true);
    	    	    	   }
    	    	    	   else
    	    	    	   {
    	    	    		   this.setEnable(false);
    	    	    	   }
    	    	    }
    	    }
    }
	public void logDesc(){
		if(type.getId()==0)
			return;
		
		logger.info("");
		logger.info("==========================================================");
		logger.info((isEnable?"Start":"Skip") +" Step : {'name': '"+type.getName()+"', 'order':'"+order+
						"', 'section':'"+sectionName+"'}");
		logger.info("----------------------------------------------------------");
		if(isEnable){
			logger.info("handler: ");
			logger.info("- "+ type.getHandler());
			logger.info("parameters: ");
			for(Entry<String, String> e:params.entrySet())
				logger.info("- "+e.getKey()+" = "+e.getValue());
			for(Entry<String, List<String>> e: paramMultiValue.entrySet())
				logger.info("- "+e.getKey()+" = "+Arrays.deepToString(e.getValue().toArray()));
			logger.info("----------------------------------------------------------");
		}
	};
	
	public StepType getType() {
		return type;
	}
	public void setType(StepType type) {
		this.type = type;
	}
	public int getOrder() {
		return order;
	}
	public void setOrder(int order) {
		this.order = order;
	}
	public String getSectionName(){
		return sectionName;
	}
	public void setSectionName(String section){
		this.sectionName=section;
	}
	public int getSectionId(){
		return sectionId;
	}
	public void setSectionId(int sectionId){
		this.sectionId=sectionId;
	}
	public boolean isEnable() {
		return isEnable;
	}
	public void setEnable(boolean isEnable) {
		this.isEnable = isEnable;
	}
	public Map<String, String> getParams() {
		return params;
	}
	public void setParams(Map<String, String> params) {
		this.params = params;
	}
	public String getParam(String key){
		return params!=null?params.get(key):null;
	}
	public String getParam(String key, String defvalue){
		return (params!=null&&params.containsKey(key))?params.get(key):defvalue;
	}
	public List<String> getParamsCompatible(String key){
		if(paramMultiValue!=null && paramMultiValue.containsKey(key))
			return paramMultiValue.get(key);
		if(params!=null && params.containsKey(key))
			return Arrays.asList(params.get(key));
		return null;
	}
	public List<String> getParamMultiValue(String key) {
		return paramMultiValue!=null?paramMultiValue.get(key):null;
	}
	public void setParamsMultiValue(Map<String, List<String>> paramMultiValue) {
		this.paramMultiValue = paramMultiValue;
	}
	public Map<String, List<String>> getParamsMultiValue(){
		return paramMultiValue;
	}
	
	@Override
	public int compareTo(TaskStep o) {
		return order-o.getOrder();
	}
}

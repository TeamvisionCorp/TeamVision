package cn.teamcat.doreamon.controller.tools;

import java.util.Map;

public class TaskStep implements Comparable<TaskStep> {
	private int type;
	private int order;
	private boolean isEnable;
	private Map<String, String> params;
	public int getType() {
		return type;
	}
	public void setType(int type) {
		this.type = type;
	}
	public int getOrder() {
		return order;
	}
	public void setOrder(int order) {
		this.order = order;
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
	
	@Override
	public int compareTo(TaskStep o) {
		return order-o.getOrder();
	}
}

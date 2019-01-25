package com.xracoon.teamcat.plugin;

import java.io.Serializable;
import java.util.List;

public class TaskSection implements Comparable<TaskSection>, Serializable {
	private static final long serialVersionUID = 3072238093818294522L;
	
	private int sectionId;
	private String sectionName;
	private List<TaskStep> steps;
	public int getSectionId() {
		return sectionId;
	}
	public void setSectionId(int sectionId) {
		this.sectionId = sectionId;
	}
	public String getSectionName() {
		return sectionName;
	}
	public void setSectionName(String sectionName) {
		this.sectionName = sectionName;
	}
	public List<TaskStep> getSteps() {
		return steps;
	}
	public void setSteps(List<TaskStep> steps) {
		this.steps = steps;
	}
	
	@Override
	public int compareTo(TaskSection o) {
		return sectionId-o.getSectionId();
	}
}

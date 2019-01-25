package cn.teamcat.doreamon.controller.tools;

import java.util.List;

public class TaskSection implements Comparable<TaskSection> {
	private int sectionId;
	private List<TaskStep> steps;
	public int getSectionId() {
		return sectionId;
	}
	public void setSectionId(int sectionId) {
		this.sectionId = sectionId;
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

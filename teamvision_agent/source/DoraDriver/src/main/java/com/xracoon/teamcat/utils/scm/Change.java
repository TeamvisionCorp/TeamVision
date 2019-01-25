package com.xracoon.teamcat.utils.scm;

public class Change {
	public static enum ChangeType {
		/** Add a new file to the project */
		A,
		/** Modify an existing file in the project (content and/or mode) */
		M,
		/** Delete an existing file from the project */
		D,
		/** Rename an existing file to a new location */
		R,
		/** Copy an existing file to a new location, keeping the original */
		C;
	}
	
	private ChangeType type;
	private String oldPath;
	private String newPath;

/*	public String getChangeDesc(){
		String desc= type==ChangeType.A ? newPath : oldPath;
		if(type==ChangeType.C || type==ChangeType.R)
			desc+="->"+newPath;
		return desc;
	}*/
	
	public ChangeType getType() {
		return type;
	}
	public void setType(ChangeType type) {
		this.type = type;
	}
	public String getOldPath() {
		return oldPath;
	}
	public void setOldPath(String oldPath) {
		this.oldPath = oldPath;
	}
	public String getNewPath() {
		return newPath;
	}
	public void setNewPath(String newPath) {
		this.newPath = newPath;
	}	
}
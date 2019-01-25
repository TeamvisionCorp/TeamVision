package com.xracoon.teamcat.driver;

import com.xracoon.util.basekit.StringEx;

public class CaseAssign {
	private long caseId;
	private String packageName;
	private String className;
	private String methodName;
	private String fullCaseName;
	private int rerunId=-1;
	
	public CaseAssign(long id, String fullCaseName){
		this.caseId=id;
		this.fullCaseName=fullCaseName;
	}
	
	public CaseAssign(long id, String fullCaseName, int rerunId){
		this.caseId=id;
		this.fullCaseName=fullCaseName;
		this.rerunId=rerunId;
	}
	public CaseAssign(long id, String packName, String className, String methodName){
		this.caseId=id;
		this.packageName=packName;
		this.className=className;
		this.methodName=methodName;
	}
	
	public int getRerunId(){
		return rerunId;
	}
	public long getCaseId() {
		return caseId;
	}
	public String getFullCaseName() {
		return StringEx.isBlank(fullCaseName)? (this.packageName+"."+this.className+"#"+this.methodName): fullCaseName;
	}
	public String getPackageName() {
		return packageName;
	}
	public String getClassName() {
		return className;
	}
	public String getMethodName() {
		return methodName;
	}
}

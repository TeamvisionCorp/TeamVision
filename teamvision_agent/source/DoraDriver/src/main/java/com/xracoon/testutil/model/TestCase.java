package com.xracoon.testutil.model;

import java.util.List;


public class TestCase extends TestBase {
	public String packName;
	public String className;
	
	public int resultCode;
	public TestStatus status=TestStatus.UNKNOWN;
	public String info="";
	
	public String cause="";
	
	public String inTime;

	public String level="";
	public String[] points; 
	public String[] tags;
	public List<String> passTags;
	
	public TestCase(){
		count=1;
	}
	public TestCase(Long id, String fullCaseName){
		this();
		this.id=id;
		int hashIdx=fullCaseName.lastIndexOf("#");
		int lastDotIdx=fullCaseName.lastIndexOf(".");
		packName=lastDotIdx>0?fullCaseName.substring(0,lastDotIdx):"";
		className=fullCaseName.substring(lastDotIdx+1, hashIdx);
		name=fullCaseName.substring(hashIdx+1);
	}
	public TestCase(Long id, String packageName, String className, String caseName){
		this();
		this.id=id;
		this.packName=packageName;
		this.className= className;
		this.name= caseName;
	}
	
	/**
	 * 将参数中指定o对象的属性值复制到当前对象
	 * @param o
	 */
	public void  copy(TestCase o)
	{
		id=o.id;
		packName=o.packName;
		className=o.className;
		status=o.status;
		
		info=(o.info==null||o.info.trim().length()==0)?null:o.info.trim();
		cause=(o.cause==null||o.cause.trim().length()==0)?null:o.cause.trim();
		inTime=o.inTime;
		
		name=o.name;
		start=o.start;
		end=o.end;
		
		count=o.count;
		pass=o.pass;
		fail=o.fail;
	}
	
	public TestCase(String pName, String cName, String mName)
	{
		packName=pName;
		className=cName;
		name=mName;
		
		count=1;
	}
	
	@Override
	public String toString()
	{
		return String.format("%s/%s#%s", packName,className,name); 
	}
	
	public String getSummary()
	{
		String str=String.format("%s\t%s\t%s/%s#%s", status,inTime,packName,className,name);
		if(status.isFail())
			str+="\n"+info;
		return str; 
	}

	public String getFullName()
	{
		StringBuilder builder=new StringBuilder();
		builder.append(packName);
		builder.append(".");
		builder.append(className);
		builder.append("#");
		builder.append(name);
		return builder.toString();
	}
	@Override
	public void update() {
		count=1;
		fail=0;
		pass=0;
		
		if(status.isFail())
			fail=1;
		else if(status==TestStatus.PASS)
			pass=1;
	}
}

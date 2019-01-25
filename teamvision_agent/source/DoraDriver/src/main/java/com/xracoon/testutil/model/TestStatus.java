package com.xracoon.testutil.model;

public enum TestStatus {

	WAIT("WAIT",0),
	UNKNOWN("UNKNOWN",0),
	IGNORE("IGNORE",1),
	ASSERT("ASSERT",2),
	ERROR("ERROR",2),
	CRASH("CRASH",2),
	PASS("PASS",3);
		
	private String text;
	private int weight;
	
	public String getText() {	return text;	}

	public boolean isFail()
	{
		if(this==TestStatus.ASSERT|| this==TestStatus.ERROR || this==TestStatus.CRASH)
			return true;
		return false;
	};
	
	private TestStatus(String text, int w)
	{
		this.text=text;
		this.weight=w;
	}
	
	public int compare(TestStatus status)
	{
		return this.weight-status.weight;
	}
}
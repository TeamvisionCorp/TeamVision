package com.xracoon.testutil.model;

import java.text.SimpleDateFormat;
import java.util.Date;

public abstract class TestBase  {
	static private SimpleDateFormat sdf=new SimpleDateFormat("yy-MM-dd hh:mm:ss");
	public Long id;
	public String name;
	public Date start;
	public Date end;
	public int age;
	
	public int count;
	public int pass;
	public int fail;
	
	public Object ext;
	
	protected String genElapse()
	{
		long elapse=end.getTime()-start.getTime();
		String elapseStr = "";
		long span = elapse / 1000;
		long s = span % 60;
		long m = span / 60 % 60;
		long h = span / 60 / 60;

		elapseStr = m + ":" + (s < 10 ? "0" : "") + s;
		if (h > 0)
			elapseStr = h + ":" + elapseStr;
		
		return elapseStr;
	}
	
	public String getElapse()
	{		
		String elapse="";
		if(start!=null && end!=null)
		{
			long span=end.getTime()-start.getTime();
			long ms=span%1000;
			long s=span/1000%60;
			long m=span/1000/60;
			elapse=ms+"ms";
			if(s>0)
				elapse=s+"s  "+elapse;
			if(m>0)
				elapse=m+"m  "+elapse;
		}
		return elapse;
	}
	
	public String getStart()
	{
		return start==null?"":sdf.format(start);
	}
	public String getEnd()
	{
		return end==null?"":sdf.format(end);
	}
	
	/**
	 * ����ͳ������
	 */
	public abstract void update();
}

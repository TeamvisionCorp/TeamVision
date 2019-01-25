package com.xracoon.testutil.model;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;

public class TestClass extends TestBase {
	public String packName;
	public Map<String, TestCase> testCases=new LinkedHashMap<String, TestCase>();
	
	public TestClass(){ }
	public TestClass(String packName, String name)
	{
		this.packName=packName;
		this.name=name;
	}
	
	@Override
	public String toString()
	{
		StringBuilder b=new StringBuilder();
		b.append("TestClass: [").append(packName).append("/").append(name).append("][");
		for(Iterator<TestCase> it=testCases.values().iterator(); it.hasNext();)
		{
			b.append(it.next().name);
			if(it.hasNext())
				b.append(", ");
		}
		b.append("]");
		return b.toString();
	}

	public void put(TestCase tcase)
	{
		testCases.put(tcase.name, tcase);
	}
	
	public TestCase get(String caseName) {
		return testCases.get(caseName);
	}
	
	@Override
	public void update() {
		count=testCases.size();
		pass=0;
		fail=0;
		for(TestCase tcase: testCases.values())
		{
			tcase.update();
			pass+=tcase.pass;
			fail+=tcase.fail;
			
//			if(tcase.start!=null && (start==null || tcase.start.getTime()<start.getTime()) )
//				start=tcase.start;
//			if(tcase.end!=null && (end==null || tcase.end.getTime()>end.getTime()))
//				end=tcase.end;
		}
	}

}

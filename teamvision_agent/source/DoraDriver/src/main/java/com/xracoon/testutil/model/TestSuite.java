package com.xracoon.testutil.model;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;

public class TestSuite extends TestBase {
	public Map<String, TestPack> testPacks=new LinkedHashMap<String,TestPack>();
	
	public String targetApp;
	public String testApp;
	public String testRunner;
	public String fullElapse;
	
	public TestSuite(){}
	public TestSuite(String name){ this.name=name;}
	
	@Override
	public String toString()
	{
		StringBuilder b=new StringBuilder();
		b.append("TestSuite: [").append(name).append("][");
		for(Iterator<TestPack> it=testPacks.values().iterator(); it.hasNext();)
		{
			b.append(it.next().name);
			if(it.hasNext())
				b.append(", ");
		}
		b.append("]");
		return b.toString();
	}

	public void put(TestCase method)
	{
		if(!testPacks.keySet().contains(method.packName))
			testPacks.put(method.packName, new TestPack(method.packName));
		testPacks.get(method.packName).put(method);
	}
	
	public TestCase get(String packName,String className, String caseName)
	{
		if(testPacks.keySet().contains(packName))
			return testPacks.get(packName).get(className,caseName);
		return null;
	}
	
	public void put(TestClass testClass)
	{
		if(!testPacks.keySet().contains(testClass.packName))
			testPacks.put(testClass.packName, new TestPack(testClass.packName));
		testPacks.get(testClass.packName).put(testClass);
	}
	
	public TestClass get(String packName,String className)
	{
		if(testPacks.keySet().contains(packName))
			return testPacks.get(packName).get(className);
		return null;
	}
	
	@Override
	public void update() {
		count=0;
		pass=0;
		fail=0;
		for(TestPack tPack: testPacks.values())
		{
			tPack.update();
			count+=tPack.count;
			pass+=tPack.pass;
			fail+=tPack.fail;
			
//			if(tPack.start!=null && (start==null || tPack.start.getTime()<start.getTime()))
//				start=tPack.start;
//			if(tPack.end!=null && (end==null || tPack.end.getTime()>end.getTime()))
//				end=tPack.end;
		}
	}
}

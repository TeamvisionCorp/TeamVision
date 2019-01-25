package com.xracoon.testutil.model;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;

public class TestPack extends TestBase {
	public Map<String, TestClass> testClasses=new LinkedHashMap<String, TestClass>();
	
	public TestPack(){}
	public TestPack(String packName){this.name=packName;}
	
	@Override
	public String toString()
	{
		StringBuilder b=new StringBuilder();
		b.append("TestPack: [").append(name).append("]");
		for(Iterator<TestClass> it=testClasses.values().iterator(); it.hasNext();)
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
		if(!testClasses.keySet().contains(method.className))
			testClasses.put(method.className, new TestClass(method.packName, method.className));
		testClasses.get(method.className).put(method);
	}
	
	public TestCase get(String className, String caseName) {
		if(testClasses.keySet().contains(className))
			return testClasses.get(className).get(caseName);
		return null;
	}
	
	public void put(TestClass testClass)
	{
		if(!testClasses.keySet().contains(testClass.name))
			testClasses.put(testClass.name, new TestClass(testClass.packName, testClass.name));
	}
	
	public TestClass get(String className) {
		if(testClasses.keySet().contains(className))
			return testClasses.get(className);
		return null;
	}
	
	@Override
	public void update() {
		count=0;
		pass=0;
		fail=0;
		for(TestClass tclass: testClasses.values())
		{
			tclass.update();
			count+=tclass.count;
			pass+=tclass.pass;
			fail+=tclass.fail;
			
//			if(tclass.start!=null && (start==null || tclass.start.getTime()<start.getTime()))
//				start=tclass.start;
//			if(tclass.end!=null && (end==null || tclass.end.getTime()>end.getTime()))
//				end=tclass.end;
		}
	}
}

package com.xracoon.teamcat.utils.testngtools.caseparser;

import com.xracoon.teamcat.driver.CaseAssign;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestSuite;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.List;
import java.util.Map;

public class TestSuiteBuilder {
	public static TestSuite parseToSuiteOfCases(List<TestCase> caselist){
		TestSuite testSuite = new TestSuite();
		for(TestCase tc:caselist)
			testSuite.put(tc);
		testSuite.update();
		return testSuite;
	}
	
	public static TestSuite parseToSuite(List<CaseAssign> caselist){
		TestSuite testSuite = new TestSuite();
		for(CaseAssign ca:caselist){
			parseSingleCaseFullName(testSuite, ca.getCaseId(), ca.getFullCaseName());
		}
		testSuite.update();
		return testSuite;
	}
	
	public static TestSuite parseToSuite(Map<Integer, CaseAssign> caseMap){
		TestSuite testSuite = new TestSuite();
		for(int id:caseMap.keySet()){
			parseSingleCaseFullName(testSuite, id, caseMap.get(id).getFullCaseName());
		}
		testSuite.update();
		return testSuite;
	}
	
	private static void parseSingleCaseFullName(TestSuite suite,long id, String casename){
		if(casename.contains("#"))	
			suite.put(parseToCase(id, casename));
		else		
			suite.put(parseToClass(casename));
	}
	
	private static TestCase parseToCase(long id, String casename){
		TestCase method = new TestCase();
		method.id=id;
		int nameBeginIndex = casename.indexOf("#");
		int classBeginIndex = getClassBeginIndex(casename);		
		method.name = casename.substring(nameBeginIndex+1);
		method.className = casename.substring(classBeginIndex+1,nameBeginIndex);
		method.packName = casename.substring(0,classBeginIndex).replace("/", ".");
		return method;
	}
	
	private static TestClass parseToClass(String casename){
		TestClass testClass = new TestClass();
		int classBeginIndex = getClassBeginIndex(casename);
		testClass.packName = casename.substring(0,classBeginIndex).replace("/", ".");
		testClass.name = casename.substring(classBeginIndex+1);
		return testClass;
	}
	
	private static int getClassBeginIndex(String casename){
		int classBeginIndex;
		if(casename.contains("/"))
			classBeginIndex = casename.lastIndexOf("/");
		else {
			classBeginIndex = casename.lastIndexOf(".");
		}
		return classBeginIndex;
	}
	
	private static TestSuite parseAllCase(String testngxmlFilePath){
		TestngConfig testngConfig = new TestngConfig(testngxmlFilePath);
		TestSuite testSuite = new TestSuite();
		File file = new File(testngConfig.javaFilepath);
		File[] files = file.listFiles();
		TestClass tClass = new TestClass();
		tClass.packName = getPackName(files[0]);
		 for(File f:files)
		 {
			 tClass.name = f.getName().replace(".java", "");
			 testSuite.put(tClass);
			 System.out.println(tClass.packName+" "+tClass.name);
		 }
		return testSuite;
	}
	
	private static String getPackName(File javaFileName){
		 String pack = "";
		 try {	
			BufferedReader breader = new BufferedReader(new FileReader(javaFileName));
			String temp = "";			
			while((temp=breader.readLine())!= null){	
				if(temp.contains("package")){
					pack = temp.substring(temp.indexOf("package")+8).replace(";", "");
					break;
				}
			}
		} catch (Exception e ) {
			e.printStackTrace();
		}
		 return pack;
	 }

}

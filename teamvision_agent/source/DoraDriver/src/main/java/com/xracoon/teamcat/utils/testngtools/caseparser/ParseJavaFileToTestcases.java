package com.xracoon.teamcat.utils.testngtools.caseparser;

import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;

import java.io.*;
import java.util.Vector;

public class ParseJavaFileToTestcases {
	 public static Vector<String> getAllTestCasesOfAllJavaFiles(TestngConfig testngConfig) throws IOException
	 {
		 File file = new File(testngConfig.javaFilepath);
		 File[] files = file.listFiles();
		 Vector<String> classNames = new Vector<String>();
		 for(File f:files)
		 {			 
			 Vector<String> testcases = getTestCasesInSingleJavaFile(testngConfig.javaFilepath+f.getName());
			 classNames.addAll(testcases);
		 }
		 return classNames;
	 }
	 
	 public static Vector<String> getAllClasses(TestngConfig testngConfig) throws IOException
	 {
		 File file = new File(testngConfig.javaFilepath);
		 File[] files = file.listFiles();
		 Vector<String> classNames = new Vector<String>();
		 for(File f:files)
		 {
			 classNames.add(f.getName().replace(".java", ""));
		 }
		 return classNames;
	 }
	 
	 public static Vector<String> getTestCasesInSingleJavaFile(String javaFileName)
	 {
		FileReader freader;
		Vector<String> testcases = new Vector<String>();
		String prefix = javaFileName.replace(".java", ":");
		try {
			freader = new FileReader(javaFileName);
			BufferedReader breader = new BufferedReader(freader);
			
			try {
				String temp = "";
				while((temp=breader.readLine())!= null)
				{	
					if(temp.contains("@Test"))
					{
						String testcase = breader.readLine();
						int beginIndex = testcase.indexOf("void ");
						int endIndex = testcase.indexOf("(");
						testcase = testcase.substring(beginIndex+5, endIndex);
						testcases.add(prefix + testcase);
					}
				}	         
			} catch (IOException e) {
				System.out.println("文件读取失败");
			}
			finally
			{
				try {
					breader.close();
					freader.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		}
		return testcases;
	 }
	 
	 public static Vector<TestCase> getAllTestcasesOfAllJavaFiles(TestngConfig testngConfig) throws IOException
	 {
		 File file = new File(testngConfig.javaFilepath);
		 File[] files = file.listFiles();
		 Vector<TestCase> allCases = new Vector<TestCase>();
		 for(File f:files)
		 {			 
			 Vector<TestCase> testcases = getTestcasesInSingleJavaFile(testngConfig.javaFilepath+f.getName());
			 allCases.addAll(testcases);
		 }
		 return allCases;
	 }
	 
	 public static Vector<TestClass> getAllClasss(TestngConfig testngConfig) throws IOException
	 {
		 File file = new File(testngConfig.javaFilepath);
		 File[] files = file.listFiles();
		 Vector<TestClass> testClasses = new Vector<TestClass>();
		 TestClass tClass = new TestClass();
		 tClass.packName = getPackName(files[0]);
		 for(File f:files)
		 {
			 tClass.name = f.getName().replace(".java", "");
			 testClasses.add(tClass);
			 System.out.println(tClass.packName+" "+tClass.name);
		 }
		 return testClasses;
	 }
	 
	 public static Vector<TestCase> getTestcasesInSingleJavaFile(String javaFileName)
	 {
		Vector<TestCase> testcases = new Vector<TestCase>();
		try {
			BufferedReader breader = new BufferedReader(new FileReader(javaFileName));
			TestCase tCase = new TestCase();
			tCase.packName = getPackName(new File(javaFileName));
			tCase.className = javaFileName.substring(javaFileName.lastIndexOf("\\")+1)
					.replace(".java", ":");
			try {
				String temp = "";
				while((temp=breader.readLine())!= null)
				{	
					if(temp.contains("@Test"))
					{
						String testcase = breader.readLine();
						tCase.name = testcase.substring(testcase.indexOf("void ")+5,
								testcase.indexOf("("));
						testcases.add(tCase);
						System.out.println(tCase.packName+" "+tCase.className+" "+tCase.name);
					}
				}	         
			} catch (IOException e) {
				System.out.println("java文件读取失败");
				e.printStackTrace();
			}
			finally
			{
				try {
					breader.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		}
		return testcases;
	 }
	 
	 private static String getPackName(File javaFileName)
	 {
		 String pack = "";
		 try {	
			BufferedReader breader = new BufferedReader(new FileReader(javaFileName));
			String temp = "";			
			while((temp=breader.readLine())!= null)
			{	
				if(temp.contains("package"))
				{
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

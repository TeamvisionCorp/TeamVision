package com.xracoon.teamcat.utils.testngtools.caseparser;

import java.io.*;
import java.util.Vector;

public class ParseTestngClass {
	 public void getAllTestCasesOfAllJavaFiles(String javaFilePath) throws IOException
	 {
		 File file = new File(javaFilePath);
		 File[] files = file.listFiles();
		 Vector<String> classNames = new Vector<String>();
		 for(File f:files)
		 {
//			 classNames.add(f.getName());
			 getTestCasesInSingleJavaFile(f.getName());
			 System.out.println(f.getName());
		 }
	 }
	 
	 public Vector<String> getTestCasesInSingleJavaFile(String javaFileName)
	 {
		FileReader freader;
		Vector<String> testcases = new Vector<String>();
		try {
			freader = new FileReader(javaFileName);
			BufferedReader breader = new BufferedReader(freader);
			
			try {
				String temp = "";
	         while((temp=breader.readLine())!= null)
	         {
	        	 if(temp.equals("@Test"))
	        	 {
	        		 String testcase = breader.readLine();
	        		 int endIndex = testcase.indexOf("(");
	        		 testcase = testcase.substring(13, endIndex);
	        		 testcases.add(testcase);
	        		 System.out.println(testcase);
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
}

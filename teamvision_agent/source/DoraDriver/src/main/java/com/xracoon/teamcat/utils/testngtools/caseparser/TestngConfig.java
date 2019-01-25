package com.xracoon.teamcat.utils.testngtools.caseparser;

public class TestngConfig {
	public static String suite = "Suite";
	public static String test = "Test";
	public static String xml = "testng.xml";
	//public static String javaFilepath = "\\src\\com\\gateside\\autotesting\\generation\\";//gat1.0
	public static String javaFilepath ="\\src\\test\\java\\com\\gateside\\autotesting\\generation\\unittest\\";
	public static String pack = javaFilepath.substring(javaFilepath.indexOf("com")).replace("\\", ".");
	public TestngConfig(String testngxmlFilePath)
	{
		this.javaFilepath = testngxmlFilePath + javaFilepath;
	}
	
	public TestngConfig(String xml,String testngxmlFilePath)
	{
		this.xml = xml;
		this.javaFilepath = testngxmlFilePath + javaFilepath;
	}
	
	public TestngConfig(String test,String xml,String testngxmlFilePath)
	{
		this.test = test;
		this.xml = xml;
		this.javaFilepath = testngxmlFilePath + javaFilepath;
	}
	
	public TestngConfig(String suite,String test,String xml,String javaFilepath)
	{
		this.suite = suite;
		this.test = test;
		this.xml = xml;
		this.javaFilepath = javaFilepath;
	}
}

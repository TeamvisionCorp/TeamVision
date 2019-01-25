package com.xracoon.teamcat.utils.testngtools.caserunner;

import com.xracoon.teamcat.utils.testngtools.caseparser.TestngConfig;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestPack;
import com.xracoon.testutil.model.TestSuite;
import com.xracoon.util.basekit.system.OS;
import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import org.dom4j.io.OutputFormat;
import org.dom4j.io.XMLWriter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

public class TestConfigTool {
	private static Logger logger = LoggerFactory.getLogger(TestConfigTool.class);
	public static void setLogger(Logger log){
		logger=log;
	}
	
    public static File createConfigFile(TestSuite testSuite,String xmlFilepath) throws IOException{
    	File file=create(testSuite, xmlFilepath);
    	logger.info("testng.xml created : "+xmlFilepath);
    	return file;
    }
    
    private static File  create(TestSuite testSuite,String xmlFilepath) throws IOException {
		TestngConfig testngConfig = new TestngConfig(xmlFilepath);
		String xmlfilepath="";
		if(OS.isUnixLike()){
			xmlfilepath= xmlFilepath +"/" + testngConfig.xml;
		}else{
			xmlfilepath= xmlFilepath +"\\" + testngConfig.xml;
		}
    	File xml = new File(xmlfilepath);
    	if(xml.exists())
    		xml.delete();
    	Document document = makeXml(testngConfig, testSuite);
        OutputFormat format = OutputFormat.createPrettyPrint();   
        format.setEncoding("UTF-8");   
        XMLWriter writer= new XMLWriter(new OutputStreamWriter(new FileOutputStream(xmlfilepath),format.getEncoding()),format);   
        writer.write( document );   
        writer.close();   
        
        return xml;
	}
	
	 private static Document makeXml(TestngConfig testngConfig,TestSuite testSuite)
	 {
		 Document document = DocumentHelper.createDocument();                                   
	     Element suite = document.addElement( "suite" )  
	                .addAttribute("name", testngConfig.suite).addAttribute("parallel", "none");   
	    
//	     Element listeners=suite.addElement("listeners");
//	     listeners.addElement("listener").addAttribute("class-name", "com.xracoon.teamcat.driver.listener.InterfaceTestListener");	
	     
	     Element test = suite.addElement( "test" )
	        		.addAttribute("name", testngConfig.test)
	                .addAttribute("verbose", "2")                      
	                .addAttribute("preserve-order", "true");  
	     
	     Element classes = test.addElement( "classes" ); 
	     makeClassInXml(testSuite, classes);
	     return document;
	 }
	 
	private static void makeClassInXml(TestSuite testSuite,Element classes)
    {
		for(String tpname:testSuite.testPacks.keySet())
		{
			TestPack tp=testSuite.testPacks.get(tpname);
			for(String tcname: tp.testClasses.keySet())
			{
				TestClass tc=tp.testClasses.get(tcname);
				Element xc=classes.addElement("class");
				xc.addAttribute("name", tc.packName+"."+tc.name);
				if(tc.testCases!=null && tc.testCases.size()>0)
				{
					Element xms=xc.addElement("methods");
					for(String tmname: tc.testCases.keySet())
					{
						TestCase tm=tc.testCases.get(tmname);
						Element xm=xms.addElement("include");
						xm.addAttribute("name", tm.name);
					}
					
					Element xexc=xms.addElement("exclude");
					xexc.addAttribute("name", ".+");
				}
			}
		}      
    }
	
}

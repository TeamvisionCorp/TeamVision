package com.xracoon.teamcat.utils.testngtools.resultparser;

import com.xracoon.teamcat.driver.CaseStatus;
import com.xracoon.teamcat.utils.testngtools.TestProcessListener;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestSuite;
import com.xracoon.util.basekit.system.OS;
import org.dom4j.Document;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

public class TestngReportTool {
	private Logger logger = LoggerFactory.getLogger(TestngReportTool.class);

	public  void setLogger(Logger log){
		logger=log;
	}
	
	public void parseTestngResults(String testOutputPath) throws Exception{
		String fileName = testOutputPath;
		if(OS.isUnixLike()){
			fileName+="/testng-results.xml";
		}else{
			fileName+="\\testng-results.xml";
		}
		
		SAXReader  builder = new SAXReader();
		Document document=null;
		try{
			InputStreamReader isr = new InputStreamReader(new FileInputStream(fileName),"gbk");
			document = builder.read(isr);
		}
		catch(Exception e){
			InputStream file = new FileInputStream(fileName);
			document = builder.read(file);
		}
		
		Element root = document.getRootElement();
		Element child = root.element("suite").element("test");
		
		@SuppressWarnings("unchecked")
		List<Object> classList = child.elements();
		for(Object e:classList)
			parseTestClass((Element)e);
	}
	
	private void parseTestClass(Element xclass) throws Exception{
		String className=xclass.attributeValue("name");
		for(Object obj:xclass.elements("test-method")){
			Element testMethod =(Element)obj;
			if(isTestCase(testMethod.attributeValue("name")))
				parseTestMethod(className, testMethod);
		}
	}
	
	public boolean isTestCase(String methodName){
		String[] exclude=new String[]{"beforeTestMethod", "beforeMethod","afterMethod", "afterClassMethod" };
		for(String str: exclude)
			if(methodName.equalsIgnoreCase(str))
				return false;
		return true;
	}
	
	private void parseTestMethod(String fullClassName,Element testMethod) throws Exception{
		int index=fullClassName.lastIndexOf(".");
		String packName=fullClassName.substring(0,index);
		String className=fullClassName.substring(index+1);
		
		String caseName=testMethod.attributeValue("name");		
		TestCase tcase=new TestCase(packName,className,caseName);
		tcase.start= parseStringToDate(testMethod, "started-at");
		tcase.end = parseStringToDate(testMethod, "finished-at");
		tcase.resultCode = getStatus(testMethod.attributeValue("status"));
		//tcase.id=
		if(tcase.resultCode==CaseStatus.FAIL){	
			Element exception = testMethod.element("exception");
			tcase.info = exception.attributeValue("class");
			tcase.cause = exception.element("full-stacktrace").getStringValue();
			
			//移除Gat的异常信息
			int v1=tcase.cause.indexOf("com.gateside.autotesting.Gat.executor");
			int v2=tcase.cause.indexOf("Caused by:");
			if(v1>=0 && v2>v1)	
				tcase.cause=tcase.cause.substring(v2);
		}
		
		logger.info("find case reuslt :   ["+tcase.resultCode+"] "+tcase.getFullName());
		fireEndCaseEvent(tcase);
	}
	
	
	private Date parseStringToDate(Element testMethod, String parseAttribute) throws ParseException{
		String time = testMethod.attributeValue(parseAttribute);
		time = time.replace("T", " ").replace("Z", "");
		SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");	
		Date s= formatter.parse(time);	
		return s;
	}
	
	private int getStatus(String caseStatus){
		int status = CaseStatus.IGNORE;
		switch (caseStatus) {
		case "PASS":
			status = CaseStatus.PASS;
			break;
		case "FAIL":
			status = CaseStatus.FAIL;
			break;
		default:
			break;
		}
		return status;
	}
	
	//------
	private Collection<TestProcessListener> listeners;
	public void addTestListener(TestProcessListener listener) {
        if (listeners == null) {
            listeners = new HashSet<TestProcessListener>();
        }
        listeners.add(listener);
    }
	public void removeTestListener(TestProcessListener listener) {
	        if (listeners == null)
	            return;
	        listeners.remove(listener);
	    }	    
	protected void fireEndCaseEvent(TestCase tcase) throws Exception {
        Iterator<TestProcessListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	TestProcessListener listener = iter.next();
            listener.end(tcase);
        }
	  }
	protected void fireStartCaseEvent(TestCase tcase) {
        Iterator<TestProcessListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	TestProcessListener listener = iter.next();
            listener.start(tcase);
        }
	  }
	protected void fireFinishedEvent(TestSuite suite)
	{
        Iterator<TestProcessListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	TestProcessListener listener = iter.next();
            listener.finish(suite);
        }
	}
}

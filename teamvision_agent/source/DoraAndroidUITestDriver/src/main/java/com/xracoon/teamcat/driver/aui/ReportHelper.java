package com.xracoon.teamcat.driver.aui;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.StringReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;
import org.xmlpull.v1.XmlSerializer;

import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestPack;
import com.xracoon.testutil.model.TestStatus;
import com.xracoon.testutil.model.TestSuite;

public class ReportHelper {
	//private Logger logger=Logger.getLogger(TestLauncher.class.getName());
	private XmlPullParserFactory serializerFactory;
	
	static private final String TAGSUITE="suite";
	static private final String ATTFULLELAPSE="full-elapse";
	
	static private final String TAGPACK="package";
	static private final String TAGCLASS="class";
	static private final String TAGCASE="test";
	static private final String TAGSTATUS="status";
	static private final String TAGINFO="msg";
	static private final String TAGCAUSE="cause";
	static private final String TAGPROCESS="process";
	
	static private final String ATTNAME="name";
	static private final String ATTINTIME="basetime";
	static private final String ATTCOUNT="count";
	static private final String ATTPASS="pass";
	static private final String ATTFAIL="fail";
	
	static private final String ATTLEVEL="level";
	static private final String ATTPOINTS="points";
	static private final String ATTTAGS="tags";
	static private final String ATTPASSTAGS="passtags";
	
	static private final String ATTSTART="start";
	static private final String ATTEND="end";
	static private final String ATTELAPSED="elapse";
	
	static private final String ATTAPPTARGET="apptarget";
	static private final String ATTAPPTEST="apptest";
	static private final String ATTTESTRUNNER="testrunner";
	
	private SimpleDateFormat attrSdf=new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSS");
	
	public ReportHelper() throws XmlPullParserException
	{
		serializerFactory=XmlPullParserFactory.newInstance();
	}
	
	public void createHtmlReport(TestSuite testSuite, String path)
	{
		
	}
	
	public void createReport(TestSuite testSuite, String path,String xml) throws XmlPullParserException, IllegalArgumentException, IllegalStateException, IOException
	{
		File reportPath=new File(path);
		if(!reportPath.exists())
			reportPath.mkdirs();
		
		BufferedWriter writer=new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(reportPath, xml)),"UTF-8"));
		XmlSerializer serializer = serializerFactory.newSerializer();
		serializer.setOutput(writer);
		serializer.startDocument("UTF-8", true);
		serializer.startTag(null, TAGSUITE);
		serializer.attribute(null, ATTCOUNT, testSuite.count+"");
		serializer.attribute(null, ATTPASS, testSuite.pass+"");
		serializer.attribute(null, ATTFAIL, testSuite.fail+"");
		
		if(testSuite.fullElapse!=null)
			serializer.attribute(null, ATTFULLELAPSE, testSuite.fullElapse);
		
		if(testSuite.start!=null)
			serializer.attribute(null, ATTSTART, attrSdf.format(testSuite.start));
		if(testSuite.end!=null)
			serializer.attribute(null, ATTEND, attrSdf.format(testSuite.end));
		
		if(testSuite.targetApp!=null && testSuite.targetApp.trim().length()>0)
			serializer.attribute(null, ATTAPPTARGET, testSuite.targetApp);
		if(testSuite.testApp!=null && testSuite.testApp.trim().length()>0)
			serializer.attribute(null, ATTAPPTEST, testSuite.testApp);
		if(testSuite.testRunner!=null && testSuite.testRunner.trim().length()>0)
			serializer.attribute(null, ATTTESTRUNNER, testSuite.testRunner);
		
		serializer.attribute(null, ATTELAPSED, testSuite.getElapse()+"");
		
		for (TestPack pack : testSuite.testPacks.values())
		{
			serializer.startTag(null, TAGPACK);
			serializer.attribute(null, ATTNAME, pack.name);
			serializer.attribute(null, ATTCOUNT, pack.count+"");
			serializer.attribute(null, ATTPASS, pack.pass+"");
			serializer.attribute(null, ATTFAIL, pack.fail+"");
			if(pack.start!=null)
				serializer.attribute(null, ATTSTART, attrSdf.format(pack.start));
			if(pack.end!=null)
				serializer.attribute(null, ATTEND, attrSdf.format(pack.end));
			
			serializer.attribute(null, ATTELAPSED, pack.getElapse()+"");
			
			for(TestClass clss: pack.testClasses.values())
			{
				serializer.startTag(null, TAGCLASS);
				serializer.attribute(null, ATTNAME, clss.name);
				serializer.attribute(null, ATTCOUNT, clss.count+"");
				serializer.attribute(null, ATTPASS, clss.pass+"");
				serializer.attribute(null, ATTFAIL, clss.fail+"");
				if(clss.start!=null)
					serializer.attribute(null, ATTSTART, attrSdf.format(clss.start));
				if(clss.end!=null)
					serializer.attribute(null, ATTEND, attrSdf.format(clss.end));
				serializer.attribute(null, ATTELAPSED, clss.getElapse()+"");
				
				for(TestCase tcase:clss.testCases.values())
				{
					serializer.startTag(null, TAGCASE);
					serializer.attribute(null, ATTNAME, tcase.name);
					serializer.attribute(null, ATTCOUNT, tcase.count+"");
					serializer.attribute(null, ATTPASS, tcase.pass+"");
					serializer.attribute(null, ATTFAIL, tcase.fail+"");
					if(tcase.start!=null)
						serializer.attribute(null, ATTSTART, attrSdf.format(tcase.start));
					if(tcase.end!=null)
						serializer.attribute(null, ATTEND, attrSdf.format(tcase.end));
					serializer.attribute(null, ATTELAPSED, tcase.getElapse()+"");
					
					if(tcase.inTime!=null && tcase.inTime.trim().length()>0)
						serializer.attribute(null, ATTINTIME, tcase.inTime);
					
					if(tcase.level!=null && tcase.level.trim().length()>0)
						serializer.attribute(null, ATTLEVEL, tcase.level);
					
					if(tcase.points!=null && tcase.points.length >0)
					{
						String pointStr="";
						for(int i=0; i<tcase.points.length; i++)
						{
							pointStr+=tcase.points[i];
							if(i<tcase.points.length-1)
								pointStr+="|";
						}
						serializer.attribute(null, ATTPOINTS, pointStr);
					}
					if(tcase.tags!=null && tcase.tags.length >0)
					{
						String tagStr="";
						for(int i=0; i<tcase.tags.length; i++)
						{
							tagStr+=tcase.tags[i];
							if(i<tcase.tags.length-1)
								tagStr+="|";
						}
						serializer.attribute(null, ATTTAGS, tagStr);
					}
					if(tcase.passTags!=null && tcase.passTags.size() >0)
					{
						String passtagStr="";
						for(int i=0; i<tcase.passTags.size(); i++)
						{
							passtagStr+=tcase.passTags.get(i);
							if(i<tcase.passTags.size()-1)
								passtagStr+="|";
						}
						serializer.attribute(null, ATTPASSTAGS, passtagStr);
					}
					
					serializer.startTag(null, TAGSTATUS);
					serializer.text(tcase.status.toString());
					serializer.endTag(null, TAGSTATUS);
					
					if(tcase.info!=null && tcase.info.trim().length()>0)
					{
						serializer.startTag(null, TAGINFO);
							serializer.cdsect(tcase.info);
						serializer.endTag(null, TAGINFO);
						
						if(tcase.cause!=null && tcase.cause.trim().length()>0)
						{
							serializer.startTag(null, TAGCAUSE);
								serializer.text(tcase.cause);
							serializer.endTag(null, TAGCAUSE);
						}
						
//						if(tcase.resolve!=null)
//						{
//							serializer.startTag(null, TAGPROCESS);
//								serializer.text(tcase.resolve.toString());
//							serializer.endTag(null, TAGPROCESS);
//						}
					}
					
					serializer.endTag(null, TAGCASE);
				}			
				serializer.endTag(null, TAGCLASS);
			}
			serializer.endTag(null, TAGPACK);
		}
		serializer.endTag(null, TAGSUITE);
		serializer.endDocument();
		writer.flush();
		writer.close();
	}
	
	public TestSuite loadReport(String path) throws DocumentException, ParseException
	{
		Document doc = new SAXReader().read(new File(path));
		TestSuite tsuite=null;
		Element xsuite=doc.getRootElement();
		if(xsuite.getName().equalsIgnoreCase(TAGSUITE))
		{
			tsuite=new TestSuite("TestSuite");
			tsuite.count=Integer.parseInt(xsuite.attribute(ATTCOUNT).getValue());
			tsuite.pass=Integer.parseInt(xsuite.attribute(ATTPASS).getValue());
			tsuite.fail=Integer.parseInt(xsuite.attribute(ATTFAIL).getValue());
			
			if(xsuite.attribute(ATTSTART)!=null)
				tsuite.start=attrSdf.parse(xsuite.attribute(ATTSTART).getValue());
			if(xsuite.attribute(ATTEND)!=null)
				tsuite.end=attrSdf.parse(xsuite.attribute(ATTEND).getValue());
			
			if(xsuite.attribute(ATTAPPTARGET)!=null)
				tsuite.targetApp=xsuite.attribute(ATTAPPTARGET).getValue();
			if(xsuite.attribute(ATTAPPTEST)!=null)
				tsuite.testApp=xsuite.attribute(ATTAPPTEST).getValue();
			if(xsuite.attribute(ATTTESTRUNNER)!=null)
				tsuite.testRunner=xsuite.attribute(ATTTESTRUNNER).getValue();
			
			for(Object opack: xsuite.elements(TAGPACK))
			{
				Element xpack=(Element)opack;
				TestPack tpack=new TestPack();
				
				tpack.name=xpack.attribute(ATTNAME).getValue();
				tpack.count=Integer.parseInt(xpack.attribute(ATTCOUNT).getValue());
				tpack.pass=Integer.parseInt(xpack.attribute(ATTPASS).getValue());
				tpack.fail=Integer.parseInt(xpack.attribute(ATTFAIL).getValue());
				
				if(xpack.attribute(ATTSTART)!=null)
					tpack.start=attrSdf.parse(xpack.attribute(ATTSTART).getValue());
				if(xpack.attribute(ATTEND)!=null)
					tpack.end=attrSdf.parse(xpack.attribute(ATTEND).getValue());
				
				tsuite.testPacks.put(tpack.name, tpack);
				
				for(Object oclass: xpack.elements(TAGCLASS))
				{
					Element xclass=(Element)oclass;
					TestClass tclass=new TestClass();
					tclass.packName=tpack.name;
					tclass.name=xclass.attribute(ATTNAME).getValue();
					tclass.count=Integer.parseInt(xclass.attribute(ATTCOUNT).getValue());
					tclass.pass=Integer.parseInt(xclass.attribute(ATTPASS).getValue());
					tclass.fail=Integer.parseInt(xclass.attribute(ATTFAIL).getValue());
					if(xclass.attribute(ATTSTART)!=null)
						tclass.start=attrSdf.parse(xclass.attribute(ATTSTART).getValue());
					if(xclass.attribute(ATTEND)!=null)
						tclass.end=attrSdf.parse(xclass.attribute(ATTEND).getValue());
					
					tpack.testClasses.put(tclass.name, tclass);
					
					for(Object ocase: xclass.elements(TAGCASE))
					{
						Element xcase=(Element)ocase;
						TestCase tcase=new TestCase();
						tcase.packName=tpack.name;
						tcase.className=tclass.name;
						tcase.name=xcase.attribute(ATTNAME).getValue();
						tcase.count=Integer.parseInt(xcase.attribute(ATTCOUNT).getValue());
						tcase.pass=Integer.parseInt(xcase.attribute(ATTPASS).getValue());
						tcase.fail=Integer.parseInt(xcase.attribute(ATTFAIL).getValue());
						if(xcase.attribute(ATTSTART)!=null)
							tcase.start=attrSdf.parse(xcase.attribute(ATTSTART).getValue());
						if(xcase.attribute(ATTEND)!=null)
							tcase.end=attrSdf.parse(xcase.attribute(ATTEND).getValue());
						if(xcase.attribute(ATTINTIME)!=null)
							tcase.inTime=xcase.attribute(ATTINTIME).getValue();
						
						tcase.status=TestStatus.valueOf(((Element)xcase.element(TAGSTATUS)).getText().trim());
						Element xinfo=null;
						if((xinfo=xcase.element(TAGINFO))!=null)
							tcase.info=xinfo.getText().trim();
						Element xcasue=null;
						if((xcasue=xcase.element(TAGCAUSE))!=null)
							tcase.cause=xcasue.getText().trim();
//						Element xprocess=null;
//						if((xprocess=xcase.element(TAGPROCESS))!=null)
//							tcase.resolve=TestResolve.valueOf(TestResolve.class, xprocess.getText().trim());
						
						if(xcase.attribute(ATTLEVEL)!=null)
							tcase.level=xcase.attribute(ATTLEVEL).getValue();
						if(xcase.attribute(ATTPOINTS)!=null)
							tcase.points=xcase.attribute(ATTPOINTS).getValue().split("\\|");
						if(xcase.attribute(ATTTAGS)!=null)
							tcase.tags=xcase.attribute(ATTTAGS).getValue().split("\\|");
						if(xcase.attribute(ATTPASSTAGS)!=null)
							tcase.passTags=new ArrayList<String>(Arrays.asList(xcase.attribute(ATTPASSTAGS).getValue().split("\\|")));
						
						tclass.testCases.put(tcase.name, tcase);
					}
				}
			}
		}
		
		return tsuite;
	}
	
	public TestSuite merge(TestSuite[] tests)
	{
		TestSuite suite=new TestSuite("mergedTestSuite");
		Date min=new Date();
		Date max=new Date(0);
		for(TestSuite s : tests)
		{
			if(s.start!=null && s.start.getTime()<min.getTime())
				min=s.start;
			if(s.end!=null && s.end.getTime()>max.getTime())
				max=s.end;
			
			for(TestPack p: s.testPacks.values())
			{
				for(TestClass c: p.testClasses.values())
				{
					for(TestCase t:c.testCases.values())
					{
						TestCase tc=s.get(p.name,c.name,t.name);
						if(tc!=null && tc.status.compare(t.status)>0)
							continue;
						suite.put(t);
					}
				}
			}
		}
		
		suite.start=min;
		suite.end=max;
		suite.update();
		return suite;
	}
	
	public void translate(String xml, InputStream xslStream, String html) throws TransformerFactoryConfigurationError, TransformerException, IOException
	{
        BufferedReader xmlReader=new BufferedReader(new InputStreamReader(new FileInputStream(new File(xml)),"UTF-8"));
        StringBuilder builder=new StringBuilder();
        String line=null;
        while((line=xmlReader.readLine())!=null)
        	builder.append(line+"\n");
        if(builder.length()>0)
        	builder.deleteCharAt(builder.length()-1);
        String xmlStr=builder.toString().replaceAll("\\n", "<br/>").replaceAll("\t", "&nbsp;&nbsp;&nbsp;&nbsp;");
        StringReader strReader=new StringReader(xmlStr);
        
        Source source=new StreamSource(strReader);  
        Source template=new StreamSource(xslStream);  
          
        PrintStream htmlStream=new PrintStream(new File(html));  
        Result result=new StreamResult(htmlStream);  
        
        Transformer transformer=TransformerFactory.newInstance().newTransformer(template);  
        transformer.transform(source, result);  
        
        htmlStream.close();
        strReader.close();
        xslStream.close();  
        xmlReader.close();  
	}
	
	public void translate(String xml,String xsl,String html ) throws TransformerFactoryConfigurationError, TransformerException, IOException
	{
		 FileInputStream xslStream=new FileInputStream(xsl); 
		 translate(xml,xslStream,html);
	}
}

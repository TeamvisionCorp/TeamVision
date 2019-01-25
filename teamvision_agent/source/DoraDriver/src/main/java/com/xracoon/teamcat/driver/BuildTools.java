package com.xracoon.teamcat.driver;

import java.io.File;
import java.util.LinkedList;
import java.util.Map;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.plist.PlistUtil;
import com.xracoon.util.basekit.plist.PropertyList;
import com.xracoon.util.basekit.system.OS;
import com.xracoon.util.basekit.system.OSMac;

public final class BuildTools {
	private static Logger logger=LoggerFactory.getLogger(BuildTools.class);
	
	private Map<String, String> javaMap=new TreeMap<>();
	private Map<String, String> gradleMap=new TreeMap<>();
	private Map<String, String> xcodeMap=new TreeMap<>();
	private String toolSearchPath;
	private String xcodeSearchPath="/Applications";
	
	private BuildTools(){};
	
	public static BuildTools bt;
	//java6*, java1.7*, java.1.6*, jdk8*, jdk1.8*, jdk.1.8*
	public static Pattern javaPattern=Pattern.compile("(java|jdk)\\.?(1\\.)?(?<version>\\d+)");
	//gradle.2.1 gradle2.10.1
	public static Pattern gradlePattern=Pattern.compile("gradle\\.?(?<version>\\d+(\\.\\d+)*)");
	public static Pattern xcodePattern=Pattern.compile("xcode\\.?(?<version>\\d+)");
	public static String DEFAULT="Default";
	
	public static BuildTools search(String rootPath){
		if(bt!=null)
			return bt;
		bt=new BuildTools();
		bt.toolSearchPath=rootPath;
		
		if(StringEx.isBlank(rootPath))
			logger.warn("path of build tools has not set yet");
		else
			bt.travelDFS(new File(rootPath));
		
		if(OS.getSingleton() instanceof OSMac)
			bt.searchXcode();
		
		return bt;
	}
	
	public File getJDKPath(String key) throws Exception{
		if(DEFAULT.equalsIgnoreCase(key))
			return null;
		
		String pathString= javaMap.get(key);
		File path=null;
		if(StringEx.isBlank(pathString) || !(path=new File(pathString)).exists())
			throw new Exception("Can't find "+key+ " in "+toolSearchPath);
		return path;
	}
	public File getGradlePath(String key) throws Exception{
		if(DEFAULT.equalsIgnoreCase(key))
			return null;
		
		String pathString= gradleMap.get(key);
		File path=null;
		if(StringEx.isBlank(pathString) || !(path=new File(pathString)).exists())
			throw new Exception("Can't find "+key+ " in "+toolSearchPath);
		return path;
	}
	public File getXcodePath(String key) throws Exception{
		if(DEFAULT.equalsIgnoreCase(key))
			return null;
		
		String pathString= xcodeMap.get(key);
		File path=null;
		if(StringEx.isBlank(pathString) || !(path=new File(pathString)).exists())
			throw new Exception("Can't find "+key+ " in "+xcodeSearchPath);
		return path;
	}
//	public static void main(String[] args){
//		BuildTools bt=BuildTools.search("D:/");
//		bt.javaMap.size();
//		bt.gradleMap.size();
//	}
	
	private void searchXcode(){
		try{
			File appPath=new File(xcodeSearchPath);
			for(File file:appPath.listFiles()){
				if(file.isDirectory()){
					String name=file.getName().toLowerCase();
					if(name.startsWith("xcode") && name.endsWith(".app")){
						File verfile=new File(file,"Contents/version.plist");
						PlistUtil parser=new PlistUtil();
						PropertyList plist=parser.parse(FilesEx.readString(verfile.getAbsolutePath()));
						String verString=plist.getData("CFBundleShortVersionString").getValue().toString();
						String ver= verString.substring(0,verString.indexOf("."));
						xcodeMap.put("Xcode-"+ver, file.getAbsolutePath());
						logger.info("--found xcode"+ver+": "+file.getAbsolutePath());
					}
				}
			}
		}catch(Exception e){
			logger.warn("Exception when search installed Xcode", e);
		}
	}
	
	private boolean matchTool(File file){
		String fileName=file.getName().toLowerCase().replaceAll("[_-]", ".");
		Matcher m=javaPattern.matcher(fileName);
		if(m.find())
			javaMap.put("JDK"+m.group("version"), file.getAbsolutePath());
		else if((m=gradlePattern.matcher(fileName)).find())
			gradleMap.put("Gradle-"+m.group("version"), file.getAbsolutePath());
		else
			return false;
		return true;
	}
	
	public void travelDFS(File rootFile){		
		for(File file:rootFile.listFiles()){
			String name=file.getName().toLowerCase();
			if(file.isDirectory() 
					&& (name.contains("java")|| name.contains("jdk") || name.contains("gradle"))
					&& !matchTool(file))
				travelDFS(file);
		}
	}
	
	public void travelBFS(File rootFile){
		LinkedList<File> q=new LinkedList<>();
		if(rootFile.isDirectory())
			q.offer(rootFile);
		File file=null;
		while((file=q.poll())!=null){
			if(!matchTool(file)){
				for(File subfile: file.listFiles()){
					if(subfile.isDirectory())
						q.offer(subfile);
				}
			}
		}
	}
}

package com.xracoon.teamcat.driver.step;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.text.ParseException;
import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;
import javax.xml.parsers.ParserConfigurationException;

import com.xracoon.teamcat.driver.step.testngsteps.TestNgWebUiStep;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.xml.sax.SAXException;
import com.dd.plist.NSDictionary;
import com.dd.plist.PropertyListFormatException;
import com.dd.plist.PropertyListParser;
import com.xracoon.teamcat.driver.AgentNotifier;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.DriverLauncher;
import com.xracoon.teamcat.plugin.TaskConfig;
import com.xracoon.teamcat.plugin.TaskStep;
import com.xracoon.teamcat.utils.AntFileUtil;
import com.xracoon.teamcat.utils.Zip;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;
import net.sf.json.JSONObject;

public abstract class BuildStep {
	
	public static Logger logger= LoggerFactory.getLogger(BuildStep.class);
	
	protected TaskStep stepConf;
	protected Map<String, Object> env=new TreeMap<>();
	protected String workspace;
	
	protected BuildStep(){};
	public abstract boolean exec() throws Exception;

	public static BuildStep fromTask(TaskStep stepConf, Map<String,Object> env) throws Exception {
		BuildStep step=null;
		try{
			Class<?> clss= DriverLauncher.class.getClassLoader().loadClass(stepConf.getType().handler);
			step= (BuildStep) clss.newInstance();
			step.stepConf=stepConf;
			step.env=env;
			step.workspace=env.get(Driver.ENV_WORKSPACE).toString();
			return step;
		}catch(Exception e){
			logger.error("step handler load failed ");
			throw e;
		}
	}
	
	protected boolean xcodeSwitch(File xcodePath) throws IOException{
		//change xcode version (root)
		String workspace=env.get(Driver.ENV_WORKSPACE).toString();
		String switchCmd="xcode-select -s "+xcodePath.getAbsolutePath();
		ExecStatus es= OS.getNewInstance().execScriptSyn(switchCmd, null, new File(workspace));
		if(es.getRetVal()!=0)
			return false;
		return true;
	}
	
	protected boolean archiveFiles(String outputFilter, int archiveType) throws Exception{
		if(StringEx.isBlank(outputFilter))
			throw new Exception("未指定产出文件");
		
		File[] files=listOutputFilterFile(outputFilter);

        //detect PackageInfo
    	for(int i=0, len=files.length; i<len; i++){
    		File f=files[i];
    		if(f.getName().toLowerCase().endsWith(".ipa")){
    			env.put(Driver.ENV_PACKAGEINFO, JSONObject.fromObject(parseIpaInfo(f)).toString());
    			break;
    		}
    		if(f.getName().toLowerCase().endsWith(".apk")){
    			break;
    		}
    	}
    	
    	//.ipa只留名字最短的
    	//files= removeDuplicateIpa(files);
    	
    	//add file prefix
    	for(int i=0, len=files.length; i<len; i++){
			File f=files[i];
			if(f.getName().toLowerCase().endsWith(".ipa")){
				files[i]=updateFileName(f);
			}
			if(f.getName().toLowerCase().endsWith(".apk")){
				files[i]=updateFileName(f);
			}
		}
    	
    	//upload
		AgentNotifier notifier=(AgentNotifier) env.get(Driver.ENV_NOTIFIER);
    	for(File f:files){		
    		if(!f.isDirectory()){
    			boolean ret=notifier.requestArchive(f.getCanonicalPath(), archiveType);
    			logger.info("  "+(ret?"[success]":"[ failed]")+"\t"+f.toString());
    		}else{
    			logger.info("  [skipfolder]\t"+f.toString());
    		}
    	}
 
    	return true;
	}
	
//	private File[] removeDuplicateIpa(File[] files){
//	   	List<File> ipas=new ArrayList<>();
//    	File resolveIpa=null;
//    	for(int i=0, len=files.length; i<len; i++){
//			File f=files[i];
//			if(f.getName().toLowerCase().endsWith(".ipa")){
//				ipas.add(f);
//				if(resolveIpa==null || f.getName().length()<resolveIpa.getName().length())
//					resolveIpa=f;
//			}
//		}
//    	ipas.remove(resolveIpa);
//    	List<File> alls=new ArrayList<>(Arrays.asList(files));
//    	alls.removeAll(ipas);
//    	return alls.toArray(new File[0]);
//	}
	
	protected File[] listOutputFilterFile(String outputFilter) throws IOException, InterruptedException{
		if(StringEx.isBlank(outputFilter))
			return new File[0];
		outputFilter=outputFilter.replaceAll("^[/\\\\]+", ""); //移除开头的斜杠
		File[] files = AntFileUtil.listAll(new File(workspace), outputFilter, null);
		logger.info(files.length+" matched archive file(s) of filter "+outputFilter);
		return files;
	}
	protected void cleanOutput(String outputFilter) throws IOException, InterruptedException{
		File[] files=listOutputFilterFile(outputFilter);
		logger.info("clean output: "+Arrays.toString(files));
		for(File f: files){
			if(f.exists())
				logger.info("- "+f+"\t"+FilesEx.deleteTree(f));
		}
	}
	protected File updateFileName(File file){
		TaskConfig config = (TaskConfig) env.get(Driver.ENV_TASKCONFIG);
		//String taskName=config.getTaskName();
		String version="HEAD";
		@SuppressWarnings("unchecked")
		Map<String, String> versionMap=(Map<String,String>)env.get(Driver.ENV_VERSIONMAP);
		if(versionMap!=null&&versionMap.size()>0)
			version=versionMap.values().iterator().next();
		
		if(version.length()==40)
			version=version.substring(0,10);
		else if(!version.equals("HEAD"))
			version="r"+version;
		String oldName=file.getName();
		String ext="";
		if(oldName.contains(".")){
			int idx=oldName.lastIndexOf(".");
			ext=oldName.substring(idx+1);
			oldName=oldName.substring(0,idx);
		}
		File newFile=new File(file.getParentFile(),oldName
				+(StringEx.isBlank(config.getTokenGroup())?"":"_"+config.getTokenGroup())
				+"_#"+config.getBuildId()+"_"+version+"."+ext);
		file.renameTo(newFile);
		return newFile;
	}
	
	private PackageInfo parseIpaInfo(File f) throws IOException, PropertyListFormatException, ParseException, ParserConfigurationException, SAXException{
		ByteArrayOutputStream baos=new ByteArrayOutputStream();
		Zip.unzip(f.getAbsolutePath(), ".app/Info.plist", baos);
		NSDictionary dict= (NSDictionary) PropertyListParser.parse(baos.toByteArray());
		PropertyListParser.saveAsXML(dict, baos);
		PackageInfo info=new PackageInfo();
		try
		{
			info.name= dict.get("CFBundleName").toString();
			info.shortVersion= dict.get("CFBundleShortVersionString").toString();
			info.version= dict.get("CFBundleVersion").toString();
			info.minSupportOS= dict.get("MinimumOSVersion").toString();
			info.identifier= dict.get("CFBundleIdentifier").toString();	
		}
		catch (Exception e) {
			logger.info("get package info fail!");
			logger.error(e.getMessage());
		}
		return info;
	}
	
	public static class PackageInfo{
		private String name;
		private String version;
		private String shortVersion;
		private String minSupportOS;
		private String identifier;
		public String getName() {
			return name;
		}
		public void setName(String name) {
			this.name = name;
		}
		public String getVersion() {
			return version;
		}
		public void setVersion(String version) {
			this.version = version;
		}
		public String getShortVersion() {
			return shortVersion;
		}
		public void setShortVersion(String shortVersion) {
			this.shortVersion = shortVersion;
		}
		public String getMinSupportOS() {
			return minSupportOS;
		}
		public void setMinSupportOS(String minSupportOS) {
			this.minSupportOS = minSupportOS;
		}
		public String getIdentifier() {
			return identifier;
		}
		public void setIdentifier(String identifier) {
			this.identifier = identifier;
		}
	}
	
	public static enum StepType{
		BASIC_INFO(0,"Basic_Info"),
		SCM_SVN(1,"Scm_Svn", ScmStep.class.getName()),
		SCM_GIT(2,"Scm_Git", ScmStep.class.getName()),
		GENERIC_SHELL(3,"Shell", ShellStep.class.getName()),
		PACKAGE_CMD(4,"Package_Cmd"), //4  在StepDriver中注册
		PACKAGE_GRADLE(5,"Package_Gradle", GradleStep.class.getName()),
		PACKAGE_IOS(6,"Package_IOS", IOSPackageStep.class.getName()),
		PACKAGE_ANT(7,"Package_Ant", AntStep.class.getName()),
		DEPLOY_FILE(8,"Deploy_File", DeployFileStep.class.getName()),
		DEPLOY_SERVICE(9,"Deploy_File", DeployServiceStep.class.getName()),
		PACKAGE_IOSCMD(10,"Package_IOS_Cmd", IOSCmdPackageStep.class.getName()),
		GENERIC_SSH(11,"SSH_Copy_Execute", SshStep.class.getName()),
		PROJECTSETTINGSCHECK(13,"Package_Settings_Check",XcodeSettingsCheckStep.class.getName()),
		TEST_INTERFACE(12,"Interface_Test"), //12  在StepDriver中注册
		WEBUI_TEST(15,"WebUi_Test");//15  在StepDriver中注册
		
		private int id;
		private String name;
		private String handler;
		public int getId(){
			return this.id;
		}
		public String getName(){
			return this.name;
		}
		public void setHandler(String handler){
			this.handler=handler;
		}
		public String getHandler(){
			return this.handler;
		}
		private StepType(int id, String name){
			this.id=id;
			this.name=name;
		}
		private StepType(int id, String name, String handler){
			this(id, name);
			this.handler=handler;
		}
		public static StepType fromId(int id) throws Exception{
			for(StepType st: StepType.values())
				if(st.id==id)
					return st;
			throw new Exception("no handlr for step type "+id);
		}
	}
}
